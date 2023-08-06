# django-horizontal-list-filter

Move list filter to  above of the changelist in django admin site.


## Install

```shell
pip install django-horizontal-list-filter
```

## Usage


**pro/settings.py**

```python
INSTALLED_APPS = [
    ...
    'django_simple_tags',
    'django_horizontal_list_filter',
    'mptt', # optional
    ...
]
```

- If using mptt, make sure that django_horizontal_list_filter is above mptt, because django_horizontal_list_filter is override mptt's template.
- If using some other third part app provides customized list filter, you may need to rewrite the filter's template to turn the result html from `ul` to `select`.


## Releases

### v0.1.2 2020/09/24

- Remove django_static_jquery3 depends. Inject our css&js into ModelAdmin.media in apps.ready step.
- Add app_requires.
- Add License file.

### v0.1.1 2020/04/28

- Fix cl context variable not provided problem.

### v0.1.0 2020/04/27

- First release.
