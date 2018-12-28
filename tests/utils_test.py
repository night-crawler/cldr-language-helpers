import codecs

from tools import utils


# noinspection PyMethodMayBeStatic
class UtilsTest:
    def test_unescape_unicode(self):
        s = utils.unescape_unicode(r'Sample\u0301')
        assert s == 'Sample' + '\u0301'
        assert len(s) == len('Sample') + 1
        assert codecs.raw_unicode_escape_encode(s[6])[0] == rb'\u0301'

    def test_strip_prefix_brackets(self):
        assert utils.strip_prefix_brackets('[[sample]') == 'sample'
        assert utils.strip_prefix_brackets('\\[[sample]') == '\\[[sample'
        assert utils.strip_prefix_brackets('[[sample\\}', '[}') == 'sample\\}'

    def test_unfold_char_range(self):
        assert utils.unfold_char_range(r'\-') == [r'\-']
        assert utils.unfold_char_range(r'a\-e') == [r'a\-e']

    def test_num_ranges(self):
        assert list(utils.iter_num_ranges([1, 2, 3, 4, 7])) == [(1, 4), (7, 7)]
        assert utils.num_ranges([1, 2, 3, 4, 7]) == [(1, 4), (7, 7)]

    def test_char_ranges(self):
        assert list(utils.iter_char_ranges([*'abcd', 'q'])) == [('a', 'd'), 'q']
        assert utils.char_ranges([*'abcd', 'q']) == [('a', 'd'), 'q']

    def test_process_cldr_chars(self):
        assert utils.process_cldr_chars(r'[ \- а-е щ  {а\u0301}]') == [' ', '-', 'а', 'а́', 'б', 'в', 'г', 'д', 'е', 'щ']

    def test_compress_chars_to_range(self):
        assert utils.compress_char_ranges(['a', 'b', 'c', 'e', 'f', 'qq']) == [('a', 'c'), 'e', 'f', 'qq']
