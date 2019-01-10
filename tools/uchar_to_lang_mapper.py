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

        uchar_to_lang_map = defaultdict(lambda: [])

        for lang_code, lang_bundle in lang_map.items():
            for exemplars_key_name in conf.EXEMPLAR_KEY_NAMES:
                exemplars = get_key_recursive(lang_map, lang_code, exemplars_key_name, [])

                for char in exemplars:
                    uchar_to_lang_map[char].append(f'{lang_code}::{exemplars_key_name}')

        return uchar_to_lang_map

    def __call__(self, do_compress_char_ranges: bool = False, **kwargs):
        return json.dump(
            self._build_uchar_to_lang_map(),
            (conf.DATA_PATH / self.filename).open('w'),
            **{'indent': 2, 'sort_keys': True, **kwargs},
        )
