import json

from . import conf

# {
#   'char_map': {
#       '<char>': [1, 2, 3, 4]
#   },
#   'lang_index': {
#       'zu_ZA::main': 709
#   }
# }
__uchar_to_lang_map = json.load(conf.UCHAR_TO_LANG_MAP_PATH.open())

# {709: 'zu_ZA::main'}
__lang_index = {v: k for k, v in __uchar_to_lang_map['lang_index'].items()}


LANG_BY_CHAR_MAP = {
    char: set(__lang_index[li].split('::')[0] for li in lang_indexes)
    for char, lang_indexes
    in __uchar_to_lang_map['char_map'].items()
}
TYPE_BY_CHAR_MAP = {
    char: set(__lang_index[li].split('::')[1] for li in lang_indexes)
    for char, lang_indexes
    in __uchar_to_lang_map['char_map'].items()
}

__uchar_to_lang_map = None
__lang_index = None


class StringAnnotator(str):
    @property
    def langs_by_index(self):
        return [
            LANG_BY_CHAR_MAP.get(char, set())
            for char in self
        ]

    @property
    def char_types_by_index(self):
        return [
            TYPE_BY_CHAR_MAP.get(char, set())
            for char in self
        ]

    def get_lang_intersection(self):
        return set.intersection(*self.langs_by_index)

    def get_char_type_intersection(self):
        return set.intersection(*self.char_types_by_index)

    def _split_by_lang_intersection(self):
        if not self:
            return

        start_pos = 0
        langs_by_index = self.langs_by_index
        langs_intersection = langs_by_index[0]

        for pos, langs_set in enumerate(langs_by_index):
            langs_intersection = langs_intersection.intersection(langs_set)
            if not langs_intersection and pos:
                yield start_pos, pos
                langs_intersection = langs_set
                start_pos = pos

        yield start_pos, len(self)

    def iter_split_by_lang_intersection(self):
        for start, stop in self._split_by_lang_intersection():
            yield self[start:stop]

    def split_by_lang_intersection(self):
        return list(self.iter_split_by_lang_intersection())
