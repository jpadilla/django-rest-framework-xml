# -*- coding: utf-8 -*-
import datetime

from decimal import Decimal
from io import StringIO

from django.test import TestCase
from django.test.utils import skipUnless
from django.utils.translation import gettext_lazy

from rest_framework_xml.compat import etree
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_xml.renderers import SOAPRenderer


class XMLRendererTestCase(TestCase):
    """
    Tests specific to the XML Renderer
    """

    _complex_data = {
        "creation_date": datetime.datetime(2011, 12, 25, 12, 45, 00),
        "name": "name",
        "sub_data_list": [
            {
                "sub_id": 1,
                "sub_name": "first"
            },
            {
                "sub_id": 2,
                "sub_name": "second"
            }
        ]
    }

    def test_render_string(self):
        """
        Test SOAP rendering.
        """
        renderer = XMLRenderer()
        content = renderer.render({'Field': 'astring'}, 'application/xml')
        self.assertXMLContains(content, '<Field>astring</Field>')

    def test_render_integer(self):
        """
        Test SOAP rendering.
        """
        renderer = XMLRenderer()
        content = renderer.render({'Field': 111}, 'application/xml')
        self.assertXMLContains(content, '<Field>111</Field>')

    def test_render_datetime(self):
        """
        Test SOAP rendering.
        """
        renderer = XMLRenderer()
        content = renderer.render({
            'Field': datetime.datetime(2011, 12, 25, 12, 45, 00)
        }, 'application/xml')
        self.assertXMLContains(content, '<Field>2011-12-25 12:45:00</Field>')

    def test_render_float(self):
        """
        Test SOAP rendering.
        """
        renderer = XMLRenderer()
        content = renderer.render({'Field': 123.4}, 'application/xml')
        self.assertXMLContains(content, '<Field>123.4</Field>')

    def test_render_decimal(self):
        """
        Test SOAP rendering.
        """
        renderer = XMLRenderer()
        content = renderer.render({'Field': Decimal('111.2')}, 'application/xml')
        self.assertXMLContains(content, '<Field>111.2</Field>')

    def test_render_none(self):
        """
        Test SOAP rendering.
        """
        renderer = XMLRenderer()
        content = renderer.render({'Field': None}, 'application/xml')
        self.assertXMLContains(content, '<Field></Field>')

    def test_render_complex_data(self):
        """
        Test SOAP rendering.
        """
        renderer = XMLRenderer()
        content = renderer.render(self._complex_data, 'application/xml')
        self.assertXMLContains(content, '<sub_name>first</sub_name>')
        self.assertXMLContains(content, '<sub_name>second</sub_name>')

    def test_render_list(self):
        renderer = XMLRenderer()
        content = renderer.render(self._complex_data, 'application/xml')
        self.assertXMLContains(content, '<sub_data_list><list-item>')
        self.assertXMLContains(content, '</list-item></sub_data_list>')

    def test_render_lazy(self):
        renderer = XMLRenderer()
        lazy = gettext_lazy('hello')
        content = renderer.render({'Field': lazy}, 'application/xml')
        self.assertXMLContains(content, '<Field>hello</Field>')

    @skipUnless(etree, 'defusedxml not installed')
    def test_render_and_parse_complex_data(self):
        """
        Test SOAP rendering.
        """
        renderer = XMLRenderer()
        content = StringIO(renderer.render(self._complex_data, 'application/xml'))

        parser = XMLParser()
        complex_data_out = parser.parse(content)
        error_msg = "complex data differs!IN:\n %s \n\n OUT:\n %s" % (repr(self._complex_data), repr(complex_data_out))
        self.assertEqual(self._complex_data, complex_data_out, error_msg)

    def assertXMLContains(self, xml, string):
        self.assertTrue(xml.startswith('<?xml version="1.0" encoding="utf-8"?>\n<root>'))
        self.assertTrue(xml.endswith('</root>'))
        self.assertTrue(string in xml, '%r not in %r' % (string, xml))


class SOAPRendererTestCase(TestCase):
    """
    Test speecific to the SOAP Renderer
    """
    _complex_data = {
        "TextSearch": "Some words",
        "ComparsionResult": [
            {
                "ResultId": 1,
                "ResultTag": "tag one"
            },
            {
                "ResultId": 2,
                "ResultTag": "tag two"
            }
        ],
        "RecordDate": datetime.datetime(2020, 4, 14, 12, 45, 00)
    }

    def test_set_schema(self):
        """
        Test set soap schema
        """
        test_tag = "SOAP-TEST"
        test_endpoint = "https://xml.com/soap"
        test_service = "soapService"

        expected_vals = {
            'xmlns:%s' % test_tag: 'http://schemas.xmlsoap.org/soap/envelope/',
            'xmlns:%s' % test_service: '%s' % test_endpoint
        }

        renderer = SOAPRenderer()
        renderer.set_schema_attrs(test_tag, test_endpoint, test_service)
        content = renderer.render({'Field': 'astring'}, 'application/xml')

        self.assertEqual(renderer.schema_attrs, expected_vals)
        print(content)
        self.assertTrue(content.startswith('<?xml version="1.0" encoding="utf-8"?>\n<SOAP-TEST'))
        self.assertTrue(content.endswith('</SOAP-TEST:Envelope>'))

    def test_render_string(self):
        """
        Test SOAP rendering.
        """
        renderer = SOAPRenderer()

        content = renderer.render({'Field': 'astring'}, 'application/xml')
        self.assertSOAPContains(content, '<Field>astring</Field>')

    def test_render_integer(self):
        """
        Test SOAP rendering.
        """
        renderer = SOAPRenderer()
        content = renderer.render({'Digit': 111}, 'application/xml')
        self.assertSOAPContains(content, '<Digit>111</Digit>')

    def test_render_datetime(self):
        """
        Test SOAP rendering.
        """
        renderer = SOAPRenderer()
        content = renderer.render({
            'Field': datetime.datetime(2011, 12, 25, 12, 45, 00)
        }, 'application/xml')
        self.assertSOAPContains(content, '<Field>2011-12-25 12:45:00</Field>')

    def test_render_float(self):
        """
        Test SOAP rendering.
        """
        renderer = SOAPRenderer()
        content = renderer.render({'Field': 123.4}, 'application/xml')
        self.assertSOAPContains(content, '<Field>123.4</Field>')

    def test_render_decimal(self):
        """
        Test SOAP rendering.
        """
        renderer = SOAPRenderer()
        content = renderer.render({'Field': Decimal('111.2')}, 'application/xml')
        self.assertSOAPContains(content, '<Field>111.2</Field>')

    def test_render_none(self):
        """
        Test SOAP rendering.
        """
        renderer = SOAPRenderer()
        content = renderer.render({'Field': None}, 'application/xml')
        self.assertSOAPContains(content, '<Field></Field>')

    def test_render_complex_data(self):
        """
        Test SOAP rendering.
        """
        renderer = SOAPRenderer()
        content = renderer.render(self._complex_data, 'application/xml')
        self.assertSOAPContains(content, '<ComparsionResult><ResultId>')
        self.assertSOAPContains(content, '</ResultTag></ComparsionResult>')

    def test_render_lazy(self):
        renderer = SOAPRenderer()
        lazy = gettext_lazy('hello')
        content = renderer.render({'Field': lazy}, 'application/xml')
        self.assertSOAPContains(content, '<Field>hello</Field>')

    def assertSOAPContains(self, xml, string):
        self.assertTrue(xml.startswith('<?xml version="1.0" encoding="utf-8"?>\n<SOAP-ENV:Envelope'))
        self.assertTrue(xml.endswith('</SOAP-ENV:Envelope>'))
        self.assertTrue(string in xml, '%r not in %r' % (string, xml))