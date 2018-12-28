import pytest

from tools.parsers import (
    MainLanguagesSerializer,
    SupplementalDataParser)

pytestmark = [
    pytest.mark.tools,
    pytest.mark.generate,
]


# noinspection PyProtectedMember,PyMethodMayBeStatic
class MainLanguagesSerializerGenerateTest:
    pytestmark = [pytest.mark.alphabets]

    def test_serialize(self):
        MainLanguagesSerializer('language_alphabets.json')(
            indent=None
        )

    def test_serialize_compress(self):
        MainLanguagesSerializer('language_alphabets_compressed.json')(
            do_compress_char_ranges=True,
            indent=None
        )


# noinspection PyProtectedMember,PyMethodMayBeStatic
class SupplementalDataParserGenerateTest:
    pytestmark = [pytest.mark.languages]

    def serialize_language_map(self, supplemental_parser: SupplementalDataParser):
        supplemental_parser.serialize_language_map()
