import json

from . import conf, utils

LANGUAGE_MAP = json.load(conf.LANGUAGE_ALPHABETS_PATH.open())

MAIN_BY_LANG_MAP = {
    lang_code: ''.join(
        sorted(utils.get_key_recursive(LANGUAGE_MAP, lang_code, 'main', []))
    )
    for lang_code in LANGUAGE_MAP
}

AUXILIARY_BY_LANG_MAP = {
    lang_code: ''.join(
        sorted(utils.get_key_recursive(LANGUAGE_MAP, lang_code, 'auxiliary', []))
    )
    for lang_code in LANGUAGE_MAP
}

INDEX_BY_LANG_MAP = {
    lang_code: ''.join(
        sorted(utils.get_key_recursive(LANGUAGE_MAP, lang_code, 'auxiliary', []))
    )
    for lang_code in LANGUAGE_MAP
}

NUMBERS_BY_LANG_MAP = {
    lang_code: ''.join(
        sorted(utils.get_key_recursive(LANGUAGE_MAP, lang_code, 'numbers', []))
    )
    for lang_code in LANGUAGE_MAP
}

PUNCTUATION_BY_LANG_MAP = {
    lang_code: ''.join(
        sorted(utils.get_key_recursive(LANGUAGE_MAP, lang_code, 'punctuation', []))
    )
    for lang_code in LANGUAGE_MAP
}

ALPHABETS_BY_LANG_MAP = {
    lang_code: ''.join(sorted({
        *INDEX_BY_LANG_MAP[lang_code],
        *MAIN_BY_LANG_MAP[lang_code],
        *AUXILIARY_BY_LANG_MAP[lang_code],
    }))
    for lang_code in LANGUAGE_MAP
}
