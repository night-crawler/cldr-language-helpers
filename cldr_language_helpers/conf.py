from pathlib import Path

BASE_DIR: Path = Path(__file__).parent
assert BASE_DIR.exists()

UCHAR_TO_LANG_MAP_PATH = BASE_DIR / 'data' / 'uchar_to_lang_map.json'
assert UCHAR_TO_LANG_MAP_PATH.exists(), f'Path {UCHAR_TO_LANG_MAP_PATH} does not exist'
