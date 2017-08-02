# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from decimal import Decimal

from django.test import TestCase
from django.test.utils import skipUnless
from django.utils.six import StringIO
from django.utils.translation import gettext_lazy
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.compat import etree


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

    _complex_order_data = {
        "creation_date": datetime.datetime(2017, 7, 1, 14, 30, 00),
        "orderId": 1,
        "positions": [
            {
                "posNo": 1,
                "amount": 3,
                "messages": [
                    {
                        "type": "O",
                        "code": "xyz"
                    },
                    {
                        "type": "L",
                        "code": "zyx"
                    }
                ]
            },
            {
                "posNo": 2,
                "amount": 1,
                "messages": [
                    {
                        "type": "O",
                        "code": "xyz"
                    },
                    {
                        "type": "L",
                        "code": "zyx"
                    }
                ]
            }
        ]
    }

    def test_render_string(self):
        """
        Test XML rendering.
        """
        renderer = XMLRenderer()
        content = renderer.render({'field': 'astring'}, 'application/xml')
        self.assertXMLContains(content, '<field>astring</field>')

    def test_render_integer(self):
        """
        Test XML rendering.
        """
        renderer = XMLRenderer()
        content = renderer.render({'field': 111}, 'application/xml')
        self.assertXMLContains(content, '<field>111</field>')

    def test_render_datetime(self):
        """
        Test XML rendering.
        """
        renderer = XMLRenderer()
        content = renderer.render({
            'field': datetime.datetime(2011, 12, 25, 12, 45, 00)
        }, 'application/xml')
        self.assertXMLContains(content, '<field>2011-12-25 12:45:00</field>')

    def test_render_float(self):
        """
        Test XML rendering.
        """
        renderer = XMLRenderer()
        content = renderer.render({'field': 123.4}, 'application/xml')
        self.assertXMLContains(content, '<field>123.4</field>')

    def test_render_decimal(self):
        """
        Test XML rendering.
        """
        renderer = XMLRenderer()
        content = renderer.render({'field': Decimal('111.2')}, 'application/xml')
        self.assertXMLContains(content, '<field>111.2</field>')

    def test_render_none(self):
        """
        Test XML rendering.
        """
        renderer = XMLRenderer()
        content = renderer.render({'field': None}, 'application/xml')
        self.assertXMLContains(content, '<field></field>')

    def test_render_complex_data(self):
        """
        Test XML rendering.
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
        content = renderer.render({'field': lazy}, 'application/xml')
        self.assertXMLContains(content, '<field>hello</field>')

    def test_render_override_list_item(self):
        renderer = XMLRenderer()
        renderer.root_tag_name = 'order'
        renderer.override_item_tag_name = True
        content = renderer.render(self._complex_order_data, 'application/xml')
        self.assertXMLContains(content, '<position>', renderer.root_tag_name)
        self.assertXMLContains(content, '<message>', renderer.root_tag_name)

    @skipUnless(etree, 'defusedxml not installed')
    def test_render_and_parse_complex_data(self):
        """
        Test XML rendering.
        """
        renderer = XMLRenderer()
        content = StringIO(renderer.render(self._complex_data, 'application/xml'))

        parser = XMLParser()
        complex_data_out = parser.parse(content)
        error_msg = "complex data differs!IN:\n %s \n\n OUT:\n %s" % (repr(self._complex_data), repr(complex_data_out))
        self.assertEqual(self._complex_data, complex_data_out, error_msg)

    def assertXMLContains(self, xml, string, root_tag='root'):
        self.assertTrue(xml.startswith('<?xml version="1.0" encoding="utf-8"?>\n<{0}>'.format(root_tag)))
        self.assertTrue(xml.endswith('</{0}>'.format(root_tag)))
        self.assertTrue(string in xml, '%r not in %r' % (string, xml))
