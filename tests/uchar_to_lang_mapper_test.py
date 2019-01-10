from tools.uchar_to_lang_mapper import (
    UcharToLangMapSerializer
)


# noinspection PyMethodMayBeStatic,PyProtectedMember
class UcharToLangMapSerializerTest:
    def test_build_uchar_to_lang_map_smoke(self):
        _map = UcharToLangMapSerializer('')._build_uchar_to_lang_map()
        assert len(_map) > 1000
