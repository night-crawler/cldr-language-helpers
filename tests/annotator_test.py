import pytest

from cldr_language_helpers.annotator import StringAnnotator

pytestmark = [pytest.mark.helper, pytest.mark.annotate]


# noinspection PyMethodMayBeStatic
class StringAnnotatorTest:
    def test_used_char_types(self):
        assert StringAnnotator('123').char_types_by_index == [{'numbers'}, {'numbers'}, {'numbers'}]

    def test_used_languages(self):
        assert 'ru_RU' in StringAnnotator('ф').langs_by_index[0]

    def test_langs(self):
        assert {'ru_RU', 'en_US', 'en', 'ru'}.issubset(StringAnnotator('йцу 123 qwe LOL').all_langs)

    def test_lang_stats(self):
        stats = StringAnnotator('qwe йцу').lang_stats
        assert stats['ru_RU'] == 3
        assert stats['ru'] == 3
        assert stats['en'] == 3
        assert stats['space'] == 1

    def test_get_lang_intersection(self):
        sa = StringAnnotator('somesortof123')
        assert 'en' in sa.langs_intersection

    def test_get_char_type_intersection(self):
        assert StringAnnotator('somesortof123').char_types_intersection == set()
        assert StringAnnotator('somesortof').char_types_intersection == {'auxiliary', 'main'}
        assert StringAnnotator(' ').char_types_intersection == {'space'}

    def test_split_by_lang_intersection(self):
        assert StringAnnotator('что-то everything как-то lol !').split_by_lang_intersection() == \
               ['что-то', ' ', 'everything', ' ', 'как-то', ' ', 'lol', ' ', '!']

        assert StringAnnotator('somesortof123').split_by_lang_intersection() == ['somesortof123']

    def test_split_by_char_type(self):
        assert StringAnnotator('qwe, 123!!!').split_by_char_type() == \
               ['qwe', ',', ' ', '123', '!!!']

    def test_has_langs(self):
        assert StringAnnotator('йцу 123 qwe LOL').has_langs('ru', 'en')

    def test_has_langs_throughout(self):
        assert StringAnnotator().has_langs_throughout('ru') is False
        assert StringAnnotator('йцу 123').has_langs_throughout('ru') is True
        assert StringAnnotator('йцу 123').has_langs_throughout('ru_RU') is True
