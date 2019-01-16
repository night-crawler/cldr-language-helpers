import json
from collections import defaultdict

from tools import conf
from tools.parsers import MainLanguagesSerializer
from tools.utils import get_key_recursive


class UcharToLangMapSerializer:
    def __init__(self, filename):
        self.filename = filename

    # noinspection PyProtectedMember
    @property
    def _lang_map(self):
        return MainLanguagesSerializer('')._parse_languages()

    def _build_uchar_to_lang_map(self):
        lang_map = self._lang_map

        lang_index_map = {}
        uchar_to_lang_map = defaultdict(lambda: set())

        for exemplars_key_name in conf.EXEMPLAR_KEY_NAMES:
            for lang_code, lang_bundle in lang_map.items():
                full_lang_name = f'{lang_code}::{exemplars_key_name}'
                if full_lang_name not in lang_index_map:
                    lang_index_map[full_lang_name] = len(lang_index_map)

                lang_index = lang_index_map[full_lang_name]

                exemplars = get_key_recursive(lang_map, lang_code, exemplars_key_name, [])

                for chars in exemplars:
                    uchar_to_lang_map[chars].add(lang_index)
                    for char in chars:
                        uchar_to_lang_map[char].add(lang_index)

        uchar_to_lang_map = {uchar: sorted(lang_indexes) for uchar, lang_indexes in uchar_to_lang_map.items()}

        return {
            'lang_index': lang_index_map,
            'char_map': uchar_to_lang_map,
        }

    def __call__(self, do_compress_char_ranges: bool = False, **kwargs):
        return json.dump(
            self._build_uchar_to_lang_map(),
            (conf.DATA_PATH / self.filename).open('w'),
            **{'indent': 2, 'sort_keys': True, **kwargs},
        )
