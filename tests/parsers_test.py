import pytest

from lxml import etree

from tools import conf
from tools.parsers import (
    CLDRExemplarCharactersSerializer, CLDRLanguageNodeSerializer,
    MainLanguagesSerializer, SupplementalDataParser
)

pytestmark = [
    pytest.mark.tools,
    pytest.mark.parsers,
]


ALL_CLDR_EXEMPLAR_FILES = list(conf.CLDR_EXEMPLARS_PATH.glob('*'))
ALL_CLDR_MAIN_FILES = list(conf.CLDR_MAIN_PATH.glob('*'))


# noinspection PyProtectedMember,PyMethodMayBeStatic
class SupplementalDataParserTest:
    def test__parse_language_data(self, supplemental_parser: SupplementalDataParser):
        assert supplemental_parser._raw_language_map

    def test__process_languages(self, supplemental_parser: SupplementalDataParser):
        lang_data = supplemental_parser._processed_language_map
        assert 'ru' in lang_data
        assert 'en' in lang_data

        assert 'bs' in lang_data
        assert 'bs_Cyrl' in lang_data
        assert 'bs_Cyrl_BA' in lang_data
        assert 'bs_Latn' in lang_data
        assert 'bs_Latn_BA' in lang_data
        # assert 'ca_ES_VALENCIA' in lang_data


# noinspection PyProtectedMember,PyMethodMayBeStatic
class CLDRLanguageNodeSerializerTest:

    @pytest.mark.parametrize('cldr_exemplar_file_path', ALL_CLDR_EXEMPLAR_FILES)
    def test__all_cldr_exemplar_files__smoke(self, cldr_exemplar_file_path: str):
        root = etree.parse(str(cldr_exemplar_file_path)).getroot()
        serializer = CLDRLanguageNodeSerializer(root)
        assert serializer()

    @pytest.mark.parametrize('cldr_main_file_path', ALL_CLDR_EXEMPLAR_FILES)
    def test__all_cldr_main_files__smoke(self, cldr_main_file_path: str):
        root = etree.parse(str(cldr_main_file_path)).getroot()
        serializer = CLDRLanguageNodeSerializer(root)
        assert serializer()

    def test__parse_layout(self, cldr_exemplar_xml_file_node):
        layout = CLDRLanguageNodeSerializer(cldr_exemplar_xml_file_node)._parse_layout()
        assert layout['characterOrder']
        assert layout['lineOrder']

    def test__parse_characters(self, cldr_exemplar_xml_file_node):
        characters = CLDRLanguageNodeSerializer(cldr_exemplar_xml_file_node)._parse_characters()
        assert characters

    def test__parse_identity(self, cldr_exemplar_xml_file_node):
        identity = CLDRLanguageNodeSerializer(cldr_exemplar_xml_file_node)._parse_identity()
        assert identity
        assert identity['language']


@pytest.fixture
def characters_node():
    return etree.fromstring(r"""
        <characters>
            <exemplarCharacters>[а-е щ ъ ы ь э ю я]</exemplarCharacters>
            <exemplarCharacters type="auxiliary">[{а\u0301} {ю\u0301} {я\u0301}]</exemplarCharacters>
            <exemplarCharacters type="index">[А У Ф Х Ц Ч Ш Щ Ы Э Ю Я]</exemplarCharacters>
            <exemplarCharacters type="numbers">[  \- , % ‰ + 0 1 2 3 4 5 6 7 8 9]</exemplarCharacters>
            <exemplarCharacters type="punctuation">[\- ‐ – — , \{ \} § @ * / \&amp; #]</exemplarCharacters>
        </characters>
        """
    )


@pytest.fixture
def characters_node_am():
    return etree.fromstring(r"""
        <characters>
            <exemplarCharacters>[ሀ ሁ ሂ ሃ ሄ ህ ሆ ለ ሉ ሊ ላ ሌ ል ሎ ሏ ሐ ሑ ሒ ሓ ሔ ሕ ሖ ሗ መ ሙ ሚ ማ ሜ ም ሞ ሟ ሠ ሡ ሢ ሣ ሤ ሥ ሦ ሧ ረ ሩ ሪ ራ ሬ ር ሮ ሯ ሰ ሱ ሲ ሳ ሴ ስ ሶ ሷ ሸ ሹ ሺ ሻ ሼ ሽ ሾ ሿ ቀ ቁ ቂ ቃ ቄ ቅ ቆ ቈ ቊ ቋ ቌ ቍ በ ቡ ቢ ባ ቤ ብ ቦ ቧ ቨ ቩ ቪ ቫ ቬ ቭ ቮ ቯ ተ ቱ ቲ ታ ቴ ት ቶ ቷ ቸ ቹ ቺ ቻ ቼ ች ቾ ቿ ኀ ኁ ኂ ኃ ኄ ኅ ኆ ኈ ኊ ኋ ኌ ኍ ነ ኑ ኒ ና ኔ ን ኖ ኗ ኘ ኙ ኚ ኛ ኜ ኝ ኞ ኟ አ ኡ ኢ ኣ ኤ እ ኦ ኧ ከ ኩ ኪ ካ ኬ ክ ኮ ኰ ኲ ኳ ኴ ኵ ኸ ኹ ኺ ኻ ኼ ኽ ኾ ወ ዉ ዊ ዋ ዌ ው ዎ ዐ ዑ ዒ ዓ ዔ ዕ ዖ ዘ ዙ ዚ ዛ ዜ ዝ ዞ ዟ ዠ ዡ ዢ ዣ ዤ ዥ ዦ ዧ የ ዩ ዪ ያ ዬ ይ ዮ ደ ዱ ዲ ዳ ዴ ድ ዶ ዷ ጀ ጁ ጂ ጃ ጄ ጅ ጆ ጇ ገ ጉ ጊ ጋ ጌ ግ ጎ ጐ ጒ ጓ ጔ ጕ ጠ ጡ ጢ ጣ ጤ ጥ ጦ ጧ ጨ ጩ ጪ ጫ ጬ ጭ ጮ ጯ ጰ ጱ ጲ ጳ ጴ ጵ ጶ ጷ ጸ ጹ ጺ ጻ ጼ ጽ ጾ ጿ ፀ ፁ ፂ ፃ ፄ ፅ ፆ ፈ ፉ ፊ ፋ ፌ ፍ ፎ ፏ ፐ ፑ ፒ ፓ ፔ ፕ ፖ ፗ]</exemplarCharacters>
            <exemplarCharacters type="auxiliary">[]</exemplarCharacters>
            <exemplarCharacters type="index" draft="contributed">[ሀ ለ ሐ መ ሠ ረ ሰ ሸ ቀ ቈ በ ቨ ተ ቸ ኀ ኈ ነ ኘ አ ከ ኰ ኸ ወ ዐ ዘ ዠ የ ደ ጀ ገ ጐ ጠ ጨ ጰ ጸ ፀ ፈ ፐ]</exemplarCharacters>
            <exemplarCharacters type="numbers">[\- , . % ‰ + 0 1 2 3 4 5 6 7 8 9]</exemplarCharacters>
            <exemplarCharacters type="punctuation">[‐ – , ፡ ፣ ፤ ፥ ፦ ! ? . ። ‹ › « » ( ) \[ \]]</exemplarCharacters>
        </characters>
        """
    )


# noinspection PyProtectedMember,PyMethodMayBeStatic
class CLDRExemplarCharactersSerializerTest:
    def test__extract_exemplar_characters(self, characters_node):
        parser = CLDRExemplarCharactersSerializer(characters_node)
        assert parser._get_main_exemplar_characters(True) == [('а', 'е'), ('щ', 'я')]
        assert parser._get_auxiliary_exemplar_characters(True) == ['а\u0301', 'ю\u0301', 'я\u0301']
        assert parser._get_index_exemplar_characters(True) == ['А', ('У', 'Щ'), 'Ы', ('Э', 'Я')]
        assert parser._get_numbers_exemplar_characters(True) == ['%', ('+', '-'), ('0', '9'), '\xa0', '‰']
        assert parser._get_punctuation_exemplar_characters(True) == [
            '#', '&', '*', ',', '-', '/', '@', '{', '}', '§', '‐', '–', '—'
        ]

    def test__extract_exemplar_characters_am(self, characters_node_am):
        parser = CLDRExemplarCharactersSerializer(characters_node_am)
        chars = parser._get_punctuation_exemplar_characters(False)
        assert '[' in chars
        assert ']' in chars

    def test_inits_with_chars(self, characters_node):
        parser = CLDRExemplarCharactersSerializer(characters_node)
        assert 'main' in parser()
        assert 'auxiliary' in parser()
        assert 'index' in parser()
        assert 'numbers' in parser()
        assert 'punctuation' in parser()


# noinspection PyProtectedMember,PyMethodMayBeStatic
class MainLanguagesSerializerGenerateTest:

    def test__parse_languages_smoke(self):
        s = MainLanguagesSerializer('trash')
        s._language_files = [
            conf.CLDR_MAIN_PATH / 'en.xml',
            conf.CLDR_MAIN_PATH / 'en_US.xml',
            conf.CLDR_MAIN_PATH / 'en_US_POSIX.xml',
        ]
        s._parse_languages()
