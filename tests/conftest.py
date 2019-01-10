import pytest

from lxml import etree

from tools import conf
from tools.parsers import SupplementalDataParser

pytestmark = [
    pytest.mark.tools,
    pytest.mark.parsers,
]


@pytest.fixture
def supplemental_parser() -> SupplementalDataParser:
    return SupplementalDataParser(conf.CLDR_SUPPLEMENTAL_DATA_PATH)


@pytest.fixture
def cldr_exemplar_xml_file_node():
    tree = etree.parse(str(conf.CLDR_EXEMPLARS_PATH / 'aai.xml'))
    return tree.getroot()


@pytest.fixture
def cldr_main_xml_file_node():
    tree = etree.parse(str(conf.CLDR_MAIN_PATH / 'af.xml'))
    return tree.getroot()


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
        """)


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
        """)


@pytest.fixture
def characters_node_ast():
    return etree.fromstring(r"""
        <characters>
            <exemplarCharacters>[a á b c d e é f g h ḥ i í l ḷ m n ñ o ó p q r s t u ú ü v x y z]</exemplarCharacters>
            <exemplarCharacters type="auxiliary">[ª à ă â å ä ã ā æ ç è ĕ ê ë ē ì ĭ î ï ī j k º ò ŏ ô ö ø ō œ ù ŭ û ū w ÿ]</exemplarCharacters>
            <exemplarCharacters type="index">[A B C D E F G H I L M N Ñ O P Q R S T U V X Y Z]</exemplarCharacters>
            <exemplarCharacters type="numbers">[\- , . % ‰ + 0 1 2 3 4 5 6 7 8 9]</exemplarCharacters>
            <exemplarCharacters type="punctuation">[\- ‐ – — , ; \: ! ¡ ? ¿ . … ' ‘ ’ &quot; “ ” « » ( ) \[ \] § @ * / \\ \&amp; # † ‡ ′ ″]</exemplarCharacters>
        </characters>
        """)
