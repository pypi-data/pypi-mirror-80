# django-dynamic-resource-admin

Add dynamic css & js resources to django's admin site.

## Install

```shell
pip install django-dynamic-resource-admin
```

## Usage

**Note:**

1. We use template override mechanism, so you MUST add app name django_dynamic_resource_admin into INSTALLED_APPS.
1. The parameter request pass to get_css&get_js is the request of this view.
1. The parameters **kwargs pass to get_css&get_js are the paramters of admin view prameters.
1. Every extra js part is wrappered with closure function, so that they will be NO local variables conflict. If you want to add a global variable, name it like: `window.xxx = 123;`.

    ```javascript
    ;(function(){
        ...your js code...
    })();
    ```
**pro/settings.py**

```python
INSTALLED_APPS = [
    ...
    'django_dynamic_resource_admin',
    ...
]
```

**app/admin.py**

```python
from django.contrib import admin
from django_dynamic_resource_admin.admin import DjangoDynamicResourceAdmin
from .models import Book


class BookAdmin(DjangoDynamicResourceAdmin, admin.ModelAdmin):
    def get_css(self, request, **kwargs):
        csses = super().get_css(request)
        csses += [
"""
body{
    background-color: red;
}
""",
        ]
        return csses

admin.site.register(Book, BookAdmin)
```
## How to add your custom css&js?

- Override get_css to add extra css.
- Override get_js to add extra js.

```python
def get_css(self, request, **kwargs):
    extra_css = super().get_css(request, **kwargs)
    extra_css += [
        """body{xxx}""",
        """.title{xxx}"""
    ]
    return extra_css

def get_js(self, request, **kwargs):
    extra_js = super().get_js(request, **kwargs):
    extra_js += [
        """window.msg="hello world";""",
        """...""",
    ]
    return extra_js
```

## Release

### v0.1.1 2020/09/25

- Fix js code wrapper from `<style></style>` to `<script type="text/javascript"></script>`.
- Add license file.

### v0.1.0 2020/03/13

- First realse.
