from pathlib import Path

BASE_DIR: Path = Path(__file__).parent.parent
assert BASE_DIR.exists()

CLDR_PATH: Path = BASE_DIR / 'cldr-release-34'
assert CLDR_PATH.exists()

CLDR_SUPPLEMENTAL_DATA_PATH: Path = CLDR_PATH / 'common' / 'supplemental' / 'supplementalData.xml'
assert CLDR_SUPPLEMENTAL_DATA_PATH.exists()

CLDR_EXEMPLARS_PATH: Path = CLDR_PATH / 'exemplars' / 'main'
assert CLDR_EXEMPLARS_PATH.exists()

CLDR_MAIN_PATH: Path = CLDR_PATH / 'common' / 'main'
assert CLDR_MAIN_PATH

PACKAGE_PATH: Path = BASE_DIR / 'cldr_language_helpers'
assert PACKAGE_PATH.exists()

DATA_PATH: Path = PACKAGE_PATH / 'data'
assert DATA_PATH.exists()

DATA_LANGUAGES_JSON: Path = DATA_PATH / 'languages.json'

EXEMPLAR_KEY_NAMES = [
    'main',
    'auxiliary',
    'index',
    'numbers',
    'punctuation',
]
