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
