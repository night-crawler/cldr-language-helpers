import pytest

from tools.parsers import MainLanguagesSerializer, SupplementalDataParser
from tools.uchar_to_lang_mapper import UcharToLangMapSerializer

pytestmark = [
    pytest.mark.tools,
    pytest.mark.generate,
]


# noinspection PyProtectedMember,PyMethodMayBeStatic
class MainLanguagesSerializerGenerateTest:
    pytestmark = [pytest.mark.alphabets]

    def test_serialize(self):
        MainLanguagesSerializer('language_alphabets.json')(
            indent=2
        )

    def test_serialize_compress(self):
        MainLanguagesSerializer('language_alphabets_compressed.json')(
            do_compress_char_ranges=True,
            indent=2
        )


# noinspection PyProtectedMember,PyMethodMayBeStatic
class SupplementalDataParserGenerateTest:
    pytestmark = [pytest.mark.languages]

    def test_serialize_language_map(self, supplemental_parser: SupplementalDataParser):
        supplemental_parser.serialize_language_map()


# noinspection PyProtectedMember,PyMethodMayBeStatic
class UcharToLangMapSerializerTest:
    pytestmark = [pytest.mark.uchar_to_lang_map]

    def test_serialize_uchar_to_lang_map(self):
        UcharToLangMapSerializer('uchar_to_lang_map.json')(
            indent=2
        )
