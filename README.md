# cldr-language-helpers

Basically this projects was designed to provide a map of 
UTF8 Block Ranges to the locale/language code.

It uses cldr.unicode.org project as its reference.

# Build

Clone the latest cldr release:

```bash
svn co http://www.unicode.org/repos/cldr/tags/release-34/ ./cldr-release-34
```

## Tests

```bash
pip install -r requirements/dev.txt
```

Then run test:

```bash
pytest
```

Tests will also populate the `cldr_language_helpers/data` directory.
Or you can use just run populate tests:
```bash
pytest -sm generate
```

## API

```python
from cldr_language_helpers.annotator import StringAnnotator

assert StringAnnotator('123').char_types_by_index == [{'numbers'}, {'numbers'}, {'numbers'}]
assert 'ru_RU' in StringAnnotator('ф').langs_by_index[0]
assert {'ru_RU', 'en_US', 'en', 'ru'}.issubset(StringAnnotator('йцу 123 qwe LOL').all_langs)

stats = StringAnnotator('qwe йцу').lang_stats
assert stats['ru_RU'] == 3
assert stats['ru'] == 3
assert stats['en'] == 3
assert stats['space'] == 1

assert 'en' in StringAnnotator('somesortof123').langs_intersection

assert StringAnnotator('somesortof123').char_types_intersection == set()
assert StringAnnotator('somesortof').char_types_intersection == {'auxiliary', 'main'}
assert StringAnnotator(' ').char_types_intersection == {'space'}

assert StringAnnotator('что-то everything как-то lol !').split_by_lang_intersection() == \
       ['что-то', ' ', 'everything', ' ', 'как-то', ' ', 'lol', ' ', '!']
assert StringAnnotator('somesortof123').split_by_lang_intersection() == ['somesortof123']


assert StringAnnotator('qwe, 123!!!').split_by_char_type() == \
       ['qwe', ',', ' ', '123', '!!!']
       
assert StringAnnotator('йцу 123 qwe LOL').has_langs('ru', 'en')

assert StringAnnotator().has_langs_throughout('ru') is False
assert StringAnnotator('йцу 123').has_langs_throughout('ru') is True
assert StringAnnotator('йцу 123').has_langs_throughout('ru_RU') is True
```