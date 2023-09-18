<div class="badges">
  <a href="https://github.com/jpadilla/django-rest-framework-xml/actions?query=workflow%3ACI">
    <img src="https://github.com/jpadilla/django-rest-framework-xml/workflows/CI/badge.svg">
  </a>
  <a href="https://pypi.python.org/pypi/djangorestframework-xml">
    <img src="https://img.shields.io/pypi/v/djangorestframework-xml.svg">
  </a>
</div>

---

# REST Framework XML

XML support for Django REST Framework

---

## Overview

XML support extracted as a third party package directly from the official Django REST Framework implementation. It requires the [defusedxml][defusedxml] package only because it safeguards against some security issues that were discovered.

**Note**: XML output provided is an ad-hoc format that isn't formally described. If you have specific XML requirements you'll need to write your own XML parsers/renderers in order to fully control the representation.

## Requirements

* Python 3.8+
* Django 3.2+
* Django REST Framework 3.14+

## Installation

Install using `pip`...

```bash
$ pip install djangorestframework-xml
```

## Example

```python
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_xml.parsers.XMLParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_xml.renderers.XMLRenderer',
    ),
}
```

You can also set the renderer and parser used for an individual view, or viewset, using the APIView class based views.

```python
from rest_framework import routers, serializers, viewsets
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (XMLParser,)
    renderer_classes = (XMLRenderer,)
```

### Sample output

```xml
<?xml version="1.0" encoding="utf-8"?>
<root>
    <list-item>
        <url>http://127.0.0.1:8000/users/1/.xml</url>
        <username>jpadilla</username>
        <email>jpadilla@example.com</email>
        <is_staff>True</is_staff>
    </list-item>
</root>
```

## Testing

Install testing requirements.

```bash
$ pip install -e '.[dev]'
```

Run with pytest.

```bash
$ pytest
```

You can also use the excellent [tox](http://tox.readthedocs.org/en/latest/) testing tool to run the tests against all supported versions of Python and Django. Install tox globally, and then simply run:

```bash
$ tox
```

## Documentation

To build the documentation, you'll need to install `mkdocs`.

```bash
$ pip install mkdocs
```

To preview the documentation:

```bash
$ mkdocs serve
Running at: http://127.0.0.1:8000/
```

To build the documentation:

```bash
$ mkdocs build
```


[defusedxml]: https://pypi.python.org/pypi/defusedxml
