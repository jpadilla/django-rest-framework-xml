# djangorestframework-xml

[![build-status-image]][travis]
[![pypi-version]][pypi]

## Overview

XML support extracted as a third party package directly from the official Django REST Framework implementation. It's built using the [defusedxml][defusedxml] package.

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
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer

class ExampleView(APIView):
    """
    A view that can accept POST requests with XML content.
    """
    parser_classes = (XMLParser,)
    renderer_classes = (XMLRenderer,)

    def post(self, request, format=None):
        return Response({'received data': request.DATA})
```

## Documentation & Support

Full documentation for the project is available at http://jpadilla.github.io/django-rest-framework-xml/.

You may also want to follow the [author][jpadilla] on Twitter.



[build-status-image]: https://secure.travis-ci.org/jpadilla/django-rest-framework-xml.png?branch=master
[travis]: http://travis-ci.org/jpadilla/django-rest-framework-xml?branch=master
[pypi-version]: https://pypip.in/version/djangorestframework-xml/badge.svg
[pypi]: https://pypi.python.org/pypi/djangorestframework-xml
[defusedxml]: https://pypi.python.org/pypi/defusedxml
[jpadilla]: https://twitter.com/jpadilla_
