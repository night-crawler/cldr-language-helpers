from cldr_language_helpers.annotator import StringAnnotator
import pytest


pytestmark = [pytest.mark.helper, pytest.mark.annotate]


class StringAnnotatorTest:
    def test_bla(self):
        sa = StringAnnotator('somesortof123')
        print(sa)
