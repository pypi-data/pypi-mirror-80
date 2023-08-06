Allows to easily index CMS pages and push them to algolia.

### Usage

Install as `pip install djangocms-algolia`.

Add the following variables to settings.py:

```python
INSTALLED_APPS = [
    'djangocms_algolia',
    'algoliasearch_django',
]
ALGOLIA = {
    'APPLICATION_ID': env.get('ALGOLIA_APPLICATION_ID', ''),
    'API_KEY': env.get('ALGOLIA_API_KEY', '')
}
# not used, but django-haystack requires it to be preset in settings.py
HAYSTACK_CONNECTIONS = {'default': {'ENGINE': 'haystack.backends.simple_backend.SimpleEngine'}}
```

You can exclude plugins from indexing by adding them to `settings.ALDRYN_SEARCH_EXCLUDED_PLUGINS`.

You can also limit the CMS pages content using `settings.ALGOLIA_SEARCH_INDEX_TEXT_LIMIT`.

### Render plan text from placeholders

This package also includes a function that helps to index django models which utilize `PlaceholderField`.

You can use it as following:

```python
from djangocms_algolia.utils import render_text_from_placeholder


class CustomModel(Model):
    placeholder = PlaceholderField('Content')

    def description(self) -> str:
        return render_text_from_placeholder(self.placeholder)
```
