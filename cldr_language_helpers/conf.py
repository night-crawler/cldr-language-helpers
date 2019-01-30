from pathlib import Path

BASE_DIR: Path = Path(__file__).parent
assert BASE_DIR.exists()

DATA_DIR: Path = BASE_DIR / 'data'
assert DATA_DIR.exists()

UCHAR_TO_LANG_MAP_PATH: Path = DATA_DIR / 'uchar_to_lang_map.json'
assert UCHAR_TO_LANG_MAP_PATH.exists(), f'Path {UCHAR_TO_LANG_MAP_PATH} does not exist'

LANGUAGE_ALPHABETS_PATH: Path = DATA_DIR / 'language_alphabets.json'
assert LANGUAGE_ALPHABETS_PATH
