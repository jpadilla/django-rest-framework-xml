# Parsers

## Setting the parsers

The default set of parsers may be set globally, using the `DEFAULT_PARSER_CLASSES` setting.  For example, the following settings would allow requests with `XML` content.

    REST_FRAMEWORK = {
        'DEFAULT_PARSER_CLASSES': (
            'rest_framework_xml.parsers.XMLParser',
        )
    }

You can also set the parsers used for an individual view, or viewset,
using the `APIView` class based views.

    from rest_framework.response import Response
    from rest_framework.views import APIView
    from rest_framework_xml.parsers import XMLParser

    class ExampleView(APIView):
        """
        A view that can accept POST requests with XML content.
        """
        parser_classes = (XMLParser,)

        def post(self, request, format=None):
            return Response({'received data': request.DATA})

Or, if you're using the `@api_view` decorator with function based views.

    @api_view(['POST'])
    @parser_classes((XMLParser,))
    def example_view(request, format=None):
        """
        A view that can accept POST requests with XML content.
        """
        return Response({'received data': request.DATA})

---

# API Reference

## XMLParser

Parses REST framework's default style of `XML` request content.

Note that the `XML` markup language is typically used as the base language for more strictly defined domain-specific languages, such as `RSS`, `Atom`, and `XHTML`.

If you are considering using `XML` for your API, you may want to consider implementing a custom renderer and parser for your specific requirements, and using an existing domain-specific media-type, or creating your own custom XML-based media-type.

Requires the `defusedxml` package to be installed.

**.media_type**: `application/xml`


# Converting values to native Python data types

N.B. This section describes behavior that has changed from version 2 upwards.

Values are *not* converted to native Python, which means that you'll get strings from the default parser. You can implement your own conversion to native data types with a custom Parser that implements a `type_convert(value)` method. This method accepts a single value and returns the converted value.

In version 1.x and earlier, conversions were done for you. To retain the original behavior, implement a Parser like below and enable this Parser in `DEFAULT_PARSER_CLASSES`:

    import datetime
    import decimal

    from rest_framework_xml.parsers import XMLParser

    class MyXMLParser(XMLParser):

        def type_convert(self, value):
            if value is None:
                return value

            try:
                return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass

            try:
                return int(value)
            except ValueError:
                pass

            try:
                return decimal.Decimal(value)
            except decimal.InvalidOperation:
                pass

             return value

Enable this in your settings:

    REST_FRAMEWORK = {
        'DEFAULT_PARSER_CLASSES': (
            'path.to.MyXMLParser',
        )
    }

Or use it in `parser_classes` or the decorator for individual class based or function based views.

    import path.to.MyXMLParser as XMLParser
