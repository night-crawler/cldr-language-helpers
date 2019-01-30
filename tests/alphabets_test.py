import pytest

from cldr_language_helpers.alphabets import ALPHABETS_BY_LANG_MAP

pytestmark = [pytest.mark.helper, pytest.mark.alphabets]


# noinspection PyMethodMayBeStatic
class AlphabetsTest:
    def test_alphabets_smoke(self):
        assert ALPHABETS_BY_LANG_MAP
        assert isinstance(ALPHABETS_BY_LANG_MAP['ru'], str)
