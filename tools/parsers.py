import json
import logging
import typing as t
from collections import OrderedDict, defaultdict
from copy import copy
from itertools import product
from pathlib import Path

from lxml import etree
from lxml.etree import Element

from tools import conf
from tools.utils import (
    compress_char_ranges, process_cldr_chars, xp_attrib, xp_node, xp_text
)

logger = logging.getLogger(__name__)


class SupplementalDataParser:
    def __init__(self, path: t.Union[str, Path]):
        super().__init__()
        self._root = etree.parse(str(path)).getroot()

    @property
    def _raw_language_map(self) -> t.DefaultDict[str, t.Dict[str, str]]:
        """
        :return: a dictionary with {<lang_code>: {<lang_options>}} mappings
        """
        lang_attrs_by_type_map = defaultdict(lambda: dict())

        el_language_data = self._root.xpath('languageData')[0]
        for el_lang in el_language_data.xpath('language'):
            attributes = copy(el_lang.attrib)
            _type = attributes.pop('type')
            lang_attrs_by_type_map[_type] = {
                **lang_attrs_by_type_map[_type],
                **attributes
            }

        # noinspection PyTypeChecker
        return lang_attrs_by_type_map

    @property
    def _processed_language_map(self) -> t.Dict[str, t.Dict[str, t.Any]]:
        lang_map = {}
        for lang, v in self._raw_language_map.items():
            territories = v.pop('territories', '').split()
            scripts = v.pop('scripts', '').split()
            lang_map[lang] = {
                **v,
                'territories': territories,
                'scripts': scripts
            }
            for script in scripts:
                lang_map[f'{lang}_{script}'] = {
                    **v,
                    'scripts': [script]
                }

            for territory in territories:
                lang_map[f'{lang}_{territory}'] = {
                    **v,
                    'territories': [territory]
                }

            for script, territory in product(scripts, territories):
                lang_map[f'{lang}_{script}_{territory}'] = {
                    **v,
                    'territories': [territory],
                    'scripts': [script],
                }

        return lang_map

    @property
    def language_map(self):
        return self._processed_language_map

    def serialize_language_map(self):
        return json.dump(
            self.language_map,
            conf.DATA_LANGUAGES_JSON.open('w'),
            indent=2
        )


class CLDRExemplarCharactersSerializer:
    r"""
    Should extract data from structure like this:

        <characters>
            <exemplarCharacters>[а б щ ъ ы ь э ю я]</exemplarCharacters>
            <exemplarCharacters type="auxiliary">[{а\u0301} {ю\u0301} {я\u0301}]</exemplarCharacters>
            <exemplarCharacters type="index">[А У Ф Х Ц Ч Ш Щ Ы Э Ю Я]</exemplarCharacters>
            <exemplarCharacters type="numbers">[  \- , % ‰ + 0 1 2 3 4 5 6 7 8 9]</exemplarCharacters>
            <exemplarCharacters type="punctuation">[\- ‐ – — , \{ \} § @ * / \&amp; #]</exemplarCharacters>
        </characters>

    Also cleans markup: [], {}, or something
    https://unicode.org/reports/tr35/tr35-general.html#Exemplars
    """

    def __init__(self, character_node: Element):
        self._node = character_node

    def __call__(self, do_compress_char_ranges: bool = False) -> t.Dict[str, t.List]:
        bundle = {
            'main': self._get_main_exemplar_characters(do_compress_char_ranges),
            'auxiliary': self._get_auxiliary_exemplar_characters(do_compress_char_ranges),
            'index': self._get_index_exemplar_characters(do_compress_char_ranges),
            'numbers': self._get_numbers_exemplar_characters(do_compress_char_ranges),
            'punctuation': self._get_punctuation_exemplar_characters(do_compress_char_ranges),
        }

        return {k: v for k, v in bundle.items() if v}

    def _get_main_exemplar_characters(self, do_compress_char_ranges: bool = False):
        el_main = xp_node(self._node, '*[@type="main" or not(@type)]')
        if el_main is None:
            return []
        return self._preprocess_chars(el_main.text, do_compress_char_ranges)

    def _safe_get_exemplar_characters(self, name: str, do_compress_char_ranges: bool = False):
        try:
            el_main = self._node.xpath(f'*[@type="{name}"]')[0]
            return self._preprocess_chars(el_main.text, do_compress_char_ranges)
        except IndexError:
            return ''

    @staticmethod
    def _preprocess_chars(chars: str, do_compress_char_ranges: bool = False):
        chars = process_cldr_chars(chars)
        if do_compress_char_ranges:
            chars = compress_char_ranges(chars)

        return chars

    def _get_auxiliary_exemplar_characters(self, do_compress_char_ranges: bool = False):
        return self._safe_get_exemplar_characters('auxiliary', do_compress_char_ranges)

    def _get_index_exemplar_characters(self, do_compress_char_ranges: bool = False):
        return self._safe_get_exemplar_characters('index', do_compress_char_ranges)

    def _get_numbers_exemplar_characters(self, do_compress_char_ranges: bool = False):
        return self._safe_get_exemplar_characters('numbers', do_compress_char_ranges)

    def _get_punctuation_exemplar_characters(self, do_compress_char_ranges: bool = False):
        return self._safe_get_exemplar_characters('punctuation', do_compress_char_ranges)


class CLDRLanguageNodeSerializer:
    def __init__(self, node):
        self._root = node

    def __call__(self, do_compress_char_ranges=False) -> t.Dict[str, t.Dict]:
        bundle = {
            **self._parse_characters(do_compress_char_ranges),
            **self._parse_layout(),
            **self._parse_identity(),
        }
        return {k: v for k, v in bundle.items() if v}

    def _parse_layout(self):
        bundle = {}
        for sub_tag in ['characterOrder', 'lineOrder']:
            val = xp_text(self._root, f'layout/orientation/{sub_tag}', None)
            val and bundle.update({sub_tag: val})

        return bundle

    def _parse_characters(self, do_compress_char_ranges: bool = False):
        el_characters = xp_node(self._root, 'characters')
        if el_characters is None:
            logger.warning('No characters node')
            return {}
        return CLDRExemplarCharactersSerializer(el_characters)(do_compress_char_ranges)

    def _parse_identity(self):
        bundle = {}

        for sub_tag in ['language', 'script', 'territory', 'variant']:
            val = xp_attrib(self._root, f'identity/{sub_tag}').get('type')
            val and bundle.update({sub_tag: val})

        return bundle


class MainLanguagesSerializer:
    def __init__(self, filename: str):
        # It seems files like uk_UA.xml inherit everything from files like uk.xml
        self._language_files: t.List[Path] = sorted(
            conf.CLDR_MAIN_PATH.glob('*'),
            key=lambda x: (len(str(x).split('_')), x)
        )
        self.filename = filename

    def _parse_languages(self, do_compress_char_ranges: bool = False):
        language_map = OrderedDict()

        for lang_file in self._language_files:
            root = etree.parse(str(lang_file)).getroot()
            full_lang_code = lang_file.name.split('.')[0]
            data = CLDRLanguageNodeSerializer(root)(do_compress_char_ranges)
            language_map[full_lang_code] = data

        return language_map

    def __call__(self, do_compress_char_ranges: bool = False, **kwargs):
        return json.dump(
            self._parse_languages(do_compress_char_ranges),
            (conf.DATA_PATH / self.filename).open('w'),
            **{'indent': 2, 'sort_keys': True, **kwargs},
        )
