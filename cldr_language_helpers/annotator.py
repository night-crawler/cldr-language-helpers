import json


UCHAR_TO_LANG_MAP = json.load(open('./data/uchar_to_lang_map.json'))


class StringAnnotator(str):
    pass
