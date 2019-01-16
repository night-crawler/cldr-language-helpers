import json
from . import conf

UCHAR_TO_LANG_MAP = json.load(conf.UCHAR_TO_LANG_MAP_PATH.open())


class StringAnnotator(str):
    pass
