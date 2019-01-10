import codecs
import itertools
import typing as t

sentinel = object()


def unescape_unicode(raw_str: str):
    """
    >>> s = r'тест\u0301'
    >>> codecs.raw_unicode_escape_encode(s)
    >>> sss = ('\\u0442\\u0435\\u0441\\u0442\\u0301', 10)
    >>> codecs.raw_unicode_escape_decode(sss[0])
    >>> 'тест́'

    :param raw_str: a raw string with unicode escapes
    :return: an unescaped unicode string
    """
    _bytes, c = codecs.raw_unicode_escape_encode(raw_str)
    _str, c = codecs.raw_unicode_escape_decode(_bytes)
    return _str


def strip_prefix_brackets(raw_str: str, brackets='[]') -> str:
    if not raw_str:
        return raw_str

    tmp = raw_str
    has_stripped = False

    if not tmp.startswith(f'\\{brackets[0]}'):
        if tmp[0] == brackets[0]:
            tmp = tmp[1:]
            has_stripped = True
    if not tmp.endswith(f'\\{brackets[1]}'):
        if tmp[-1] == brackets[-1]:
            tmp = tmp[:-1]
            has_stripped = True

    if has_stripped:
        return strip_prefix_brackets(tmp, brackets)

    return tmp


def xp_node(root, xpath):
    try:
        return root.xpath(xpath)[0]
    except IndexError:
        return None


def xp_attrib(node, xpath, default=None):
    try:
        return node.xpath(xpath)[0].attrib
    except IndexError:
        return default or {}


def xp_text(node, xpath, default=''):
    try:
        return node.xpath(xpath)[0].text
    except IndexError:
        return default


def iter_num_ranges(list_of_integers: t.Iterable[int]) -> t.Generator[t.Tuple[int, int], None, None]:
    """
    Compresses a given list of integers to a list of range tuples.
    >>> list(iter_num_ranges([1, 2, 3, 4, 7]))
    >>> [(1, 4), (7, 7)]
    """
    for a, b in itertools.groupby(enumerate(list_of_integers), lambda v: v[1] - v[0]):
        b = list(b)
        yield b[0][1], b[-1][1]


def num_ranges(list_of_integers: t.Iterable[int]):
    """
    >>> num_ranges([1, 2, 3, 4, 7])
    >>> [(1, 4), (7, 7)]
    """
    return list(iter_num_ranges(list_of_integers))


def iter_char_ranges(list_of_chars: t.Iterable[str]):
    """
    Compresses a given list to a char ranges with some optimizations.
    >>> list(iter_char_ranges([*'abcd', 'q']))
    >>> [('a', 'd'), 'q']
    """
    for start, end in iter_num_ranges(map(ord, list_of_chars)):
        if start == end:
            yield chr(start)
        elif end - start == 1:
            yield chr(start)
            yield chr(end)
        else:
            yield chr(start), chr(end)


def char_ranges(list_of_chars):
    """
    >>> char_ranges([*'abcd', 'q'])
    >>> [('a', 'd'), 'q']
    """
    return list(iter_char_ranges(list_of_chars))


def unfold_char_range(char_range: str):
    _id = f'{id(char_range)}'
    ranges = [
        ch.replace(_id, r'\-')
        for ch in char_range.replace(r'\-', _id).split('-') if ch
    ]

    if len(ranges) != 2:
        return [char_range]

    range_start, range_end = ord(ranges[0]), ord(ranges[1])

    chars = []
    for ch_code in range(range_start, range_end + 1):
        chars.append(chr(ch_code))

    return chars


def remove_escapes(raw_str: str) -> str:
    if raw_str == '\\' * 2:
        return '\\'
    return raw_str.lstrip('\\')


def process_cldr_chars(chars: str) -> t.List[str]:
    r"""
    >>> process_cldr_chars('[\- а-е щ  {а\u0301}]')
    >>> ['-', 'а', 'а́', 'б', 'в', 'г', 'д', 'е', 'щ']
    >>> assert len(process_cldr_chars('[\- а-е щ  {а\u0301}]')[2]) == 2
    """
    chars = strip_prefix_brackets(chars, '[]')
    chars = unescape_unicode(chars)

    # split explicitly by ' ' in order to protect other whitespace characters
    chars = list(set(chars.split(' ')))

    try:
        chars.remove('')
        chars.append(' ')
    except ValueError:
        pass

    chars = [strip_prefix_brackets(ch, '{}') for ch in chars]
    chars = [remove_escapes(ch) for ch in chars]

    chars = sorted(
        c
        for ch in chars
        for c in unfold_char_range(ch)
    )

    return chars


def compress_char_ranges(chars: t.List[str]) -> t.List[str]:
    """
    A wrapper around char_ranges just to drop all strings with length != 1
    >>> compress_char_ranges(['a', 'b', 'c', 'e', 'f', 'qq'])
    >>> [('a', 'c'), 'e', 'f', 'qq']
    """
    single_chars = filter(lambda ch: len(ch) == 1, chars)
    other_chars = filter(lambda ch: len(ch) != 1, chars)

    return [
        *char_ranges(single_chars),
        *other_chars
    ]


def get_key_recursive(lang_map, lang_code, key_name, default=None):
    """
    >>> lang_map = {
    >>>     'ru': {'first': ['a']},
    >>>     'ru_RU': {'second': ['b']},
    >>>     'ru_RU_SOMETHING': {},
    >>> }
    >>> assert get_key_recursive(lang_map, 'ru_RU_SOMETHING', 'first', 1) == ['a']
    >>> assert get_key_recursive(lang_map, 'ru_RU_SOMETHING', 'bla', 1) == 1
    >>> assert get_key_recursive(lang_map, 'ru_RU', 'second', 1) == ['b']
    """
    key_val = lang_map.get(lang_code, {}).get(key_name, sentinel)

    if key_val is not sentinel:
        return key_val

    parts = lang_code.split('_')
    parts.pop()
    if not parts:
        return default

    _lang_code = '_'.join(parts)
    return get_key_recursive(lang_map, _lang_code, key_name, default)
