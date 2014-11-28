# REST Framework XML

[![build-status-image]][travis]
[![pypi-version]][pypi]

**XML support for Django REST Framework**

Full documentation for the project is available at [http://jpadilla.github.io/django-rest-framework-xml][docs].

## Overview

XML support extracted as a third party package directly from the official Django REST Framework implementation. It requires the [defusedxml][defusedxml] package only because it safeguards against some security issues that were discovered.

## Requirements

* Python (2.7, 3.3, 3.4)
* Django (1.6, 1.7)
* Django REST Framework (2.4.3, 2.4.4, 3.0-beta)

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

## Documentation & Support

Full documentation for the project is available at [http://jpadilla.github.io/django-rest-framework-xml][docs].

You may also want to follow the [author][jpadilla] on Twitter.


[build-status-image]: https://secure.travis-ci.org/jpadilla/django-rest-framework-xml.png?branch=master
[travis]: http://travis-ci.org/jpadilla/django-rest-framework-xml?branch=master
[pypi-version]: https://pypip.in/version/djangorestframework-xml/badge.svg
[pypi]: https://pypi.python.org/pypi/djangorestframework-xml
[defusedxml]: https://pypi.python.org/pypi/defusedxml
[docs]: http://jpadilla.github.io/django-rest-framework-xml
[jpadilla]: https://twitter.com/jpadilla_
