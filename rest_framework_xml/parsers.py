"""
Provides XML parsing support.
"""
from __future__ import unicode_literals
import datetime
import decimal

from django.conf import settings
from django.utils import six
from rest_framework.exceptions import ParseError
from rest_framework.parsers import BaseParser

from .compat import etree


class XMLParser(BaseParser):
    """
    XML parser.
    """

    media_type = 'application/xml'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as XML and returns the resulting data.
        """
        assert etree, 'XMLParser requires defusedxml to be installed'

        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        parser = etree.DefusedXMLParser(encoding=encoding)
        try:
            tree = etree.parse(stream, parser=parser, forbid_dtd=True)
        except (etree.ParseError, ValueError) as exc:
            raise ParseError('XML parse error - %s' % six.text_type(exc))
        data = self._xml_convert(tree.getroot())

        return data

    def _xml_convert(self, element):
        """
        convert the xml `element` into the corresponding python object
        """

        parent_container = dict()

        if element.getchildren():
            # recursively check for child elements
            child_container = []
            for child in element:
                child_container.append(self._xml_convert(child))

            parent_container.update({element.tag: child_container})

        else:
            parent_container.update({element.tag: element.text})

        return parent_container

    def _type_convert(self, value):
        """
        Converts the value returned by the XMl parse into the equivalent
        Python type
        """
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
