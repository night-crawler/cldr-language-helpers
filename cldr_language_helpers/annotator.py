import json
import re
import typing as t
from collections import defaultdict
from functools import reduce

from funcy import cached_property

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
ALL_LANGUAGES = set(
    li.split('::')[0]
    for li in __uchar_to_lang_map['lang_index'].keys()
)

__uchar_to_lang_map = None
__lang_index = None
__sentinel = object()


def get_possible_langs_by_char(char):
    langs_set = LANG_BY_CHAR_MAP.get(char, __sentinel)
    if langs_set is not __sentinel:
        return langs_set

    if re.match(r'\s', char):
        return ALL_LANGUAGES

    return {'unknown'}


def get_possible_char_types_by_char(char):
    char_types = TYPE_BY_CHAR_MAP.get(char, __sentinel)
    if char_types is not __sentinel:
        return char_types

    if re.match(r'\s', char):
        return {'space'}

    return {'unknown'}


class StringAnnotator(str):
    @cached_property
    def langs_by_index(self) -> t.List[t.Set[str]]:
        return [get_possible_langs_by_char(char) for char in self]

    @cached_property
    def char_types_by_index(self) -> t.List[t.Set[str]]:
        return [get_possible_char_types_by_char(char) for char in self]

    @cached_property
    def all_langs(self) -> t.Set[str]:
        return reduce(lambda x, y: x | y, self.langs_by_index)

    @cached_property
    def all_char_types(self):
        return reduce(lambda x, y: x | y, self.char_types_by_index)

    @cached_property
    def langs_intersection(self):
        return set.intersection(*self.langs_by_index)

    @cached_property
    def char_types_intersection(self):
        return set.intersection(*self.char_types_by_index)

    @cached_property
    def lang_stats(self) -> t.Dict[str, int]:
        stats = defaultdict(lambda: 0)
        for lbi, is_space in zip(self.langs_by_index, self.spaces_by_index):
            if is_space:
                stats['space'] += 1
                continue

            for lang in lbi:
                stats[lang] += 1
        return stats

    @cached_property
    def spaces_by_index(self):
        return [bool(re.match(r'\s', char)) for char in self]

    def has_langs(self, *langs) -> bool:
        if not self:
            return False
        return set(langs).issubset(self.all_langs)

    def has_langs_throughout(self, *langs) -> bool:
        if not self:
            return False

        langs = set(langs)
        for lbi in self.langs_by_index:
            if lbi == {'space'}:
                continue

            if not langs.issubset(lbi):
                return False
        return True

    def _split_by_char_type_ranges(self):
        if not self:
            return

        def reducer(state, item):
            pos, char_types = item

            if 'numbers' in char_types:
                char_type = 'numbers'
            elif {'main', 'index', 'auxiliary'} & char_types:
                char_type = 'regular'
            elif 'punctuation' in char_types:
                char_type = 'punctuation'
            elif 'space' in char_types:
                char_type = 'space'
            else:
                char_type = 'unknown'

            if not state:
                return [[pos, pos + 1, char_type]]

            if state[-1][2] == char_type:
                state[-1][1] = pos + 1
                return state
            else:
                state.append([pos, pos + 1, char_type])
                return state

        return reduce(reducer, enumerate(self.char_types_by_index), [])

    def iter_split_by_char_type(self):
        for start, stop, _type in self._split_by_char_type_ranges():
            yield self[start:stop]

    def split_by_char_type(self):
        return list(self.iter_split_by_char_type())

    def _split_by_lang_intersection_ranges(self):
        if not self:
            return

        def reducer(state, item):
            pos, [langs_set, is_space] = item

            if not state:
                return [[pos, pos + 1, langs_set, is_space]]

            prev_start, prev_finish, prev_intersection, prev_is_space = state[-1]
            intersection = prev_intersection & langs_set

            if is_space:
                if prev_is_space:
                    state[-1][1] = pos + 1
                    return state
                return state + [[pos, pos + 1, langs_set, is_space]]

            if prev_is_space:
                return state + [[pos, pos + 1, langs_set, is_space]]

            if intersection:
                state[-1][1] = pos + 1
                state[-1][2] = intersection
                return state

            return state + [[pos, pos + 1, langs_set, is_space]]

        return reduce(reducer, enumerate(zip(self.langs_by_index, self.spaces_by_index)), [])

    def iter_split_by_lang_intersection(self):
        for start, stop, *rest in self._split_by_lang_intersection_ranges():
            yield self[start:stop]

    def split_by_lang_intersection(self):
        return list(self.iter_split_by_lang_intersection())
