import pytest

from cldr_language_helpers.annotator import StringAnnotator

pytestmark = [pytest.mark.helper, pytest.mark.annotate]


# noinspection PyMethodMayBeStatic
class StringAnnotatorTest:
    def test_used_char_types(self):
        assert StringAnnotator('123').char_types_by_index == [{'numbers'}, {'numbers'}, {'numbers'}]

    def test_used_languages(self):
        assert 'ru_RU' in StringAnnotator('ф').langs_by_index[0]

    def test_get_lang_intersection(self):
        sa = StringAnnotator('somesortof123')
        assert 'en' in sa.get_lang_intersection()

    def test_get_char_type_intersection(self):
        assert StringAnnotator('somesortof123').get_char_type_intersection() == set()
        assert StringAnnotator('somesortof').get_char_type_intersection() == {'auxiliary', 'main'}
        assert StringAnnotator(' ').get_char_type_intersection() == set()

    def test__split_by_lang_intersection(self):
        s = list(StringAnnotator('что-то everything как-то lol !').split_by_lang_intersection())
        print(s)
