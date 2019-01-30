sentinel = object()


def get_key_recursive(lang_map, lang_code, key_name, default=None):
    """
    >>> lang_map = {
    >>>     'ru': {'first': ['a']},
    >>>     'ru_RU': {'second': ['b']},
    >>>     'ru_RU_SOMETHING': {},
    >>> }
    >>> assert get_key_recursive(lang_map, 'ru_RU_SOMETHING', 'first', 1) == ['a']
    >>> assert get_key_recursive(lang_map, 'ru_RU_SOMETHING', 'bla', 1) == 1
    >>> assert get_key_recursive(lang_map, 'ru_RU', 'second', 1) == ['b']
    """
    key_val = lang_map.get(lang_code, {}).get(key_name, sentinel)

    if key_val is not sentinel:
        return key_val

    parts = lang_code.split('_')
    parts.pop()
    if not parts:
        return default

    _lang_code = '_'.join(parts)
    return get_key_recursive(lang_map, _lang_code, key_name, default)
