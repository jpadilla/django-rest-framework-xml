# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime


from django.test import TestCase
from django.utils import unittest
from django.utils.six.moves import StringIO
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.compat import etree


class TestXMLParser(TestCase):
    def setUp(self):
        self._input = StringIO(
            '<?xml version="1.0" encoding="utf-8"?>'
            '<root>'
            '<field_a>121.0</field_a>'
            '<field_b>dasd</field_b>'
            '<field_c></field_c>'
            '<field_d>2011-12-25 12:45:00</field_d>'
            '</root>'
        )
        self._data = {
            'field_a': 121,
            'field_b': 'dasd',
            'field_c': None,
            'field_d': datetime.datetime(2011, 12, 25, 12, 45, 00)
        }
        self._complex_data_input = StringIO(
            '<?xml version="1.0" encoding="utf-8"?>'
            '<root>'
            '<creation_date>2011-12-25 12:45:00</creation_date>'
            '<sub_data_list>'
            '<list-item><sub_id>1</sub_id><sub_name>first</sub_name></list-item>'
            '<list-item><sub_id>2</sub_id><sub_name>second</sub_name></list-item>'
            '</sub_data_list>'
            '<name>name</name>'
            '</root>'
        )
        self._complex_data = {
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
        self._invalid_list_input = StringIO(
            '<?xml version="1.0" encoding="utf-8"?>'
            '<root>'
            '<list>'
            '<list-item><sub_id>1</sub_id><sub_name>first</sub_name></list-item>'
            '<list-item2><sub_id>2</sub_id><sub_name>second</sub_name></list-item2>'
            '<list-item2><sub_id>3</sub_id><sub_name>third</sub_name></list-item2>'
            '</list>'
            '</root>'
        )
        self._invalid_list_output = {
            "list": {
                "list-item": {
                    "sub_id": 1,
                    "sub_name": "first"
                },
                "list-item2": {
                    "sub_id": 3,
                    "sub_name": "third"
                }
            }
        }
        self._valid_list_input = StringIO(
            '<?xml version="1.0" encoding="utf-8"?>'
            '<root>'
            '<list>'
            '<list-item><sub_id>1</sub_id><sub_name>first</sub_name></list-item>'
            '<list-item><sub_id>2</sub_id><sub_name>second</sub_name></list-item>'
            '</list>'
            '</root>'
        )
        self._valid_list_output = {
            "list": [
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

    @unittest.skipUnless(etree, 'defusedxml not installed')
    def test_parse(self):
        parser = XMLParser()
        data = parser.parse(self._input)
        self.assertEqual(data, self._data)

    @unittest.skipUnless(etree, 'defusedxml not installed')
    def test_complex_data_parse(self):
        parser = XMLParser()
        data = parser.parse(self._complex_data_input)
        self.assertEqual(data, self._complex_data)

    @unittest.skipUnless(etree, 'defusedxml not installed')
    def test_invalid_list_parse(self):
        parser = XMLParser()
        data = parser.parse(self._invalid_list_input)
        self.assertEqual(data, self._invalid_list_output)

    @unittest.skipUnless(etree, 'defusedxml not installed')
    def test_valid_list_parse(self):
        parser = XMLParser()
        data = parser.parse(self._valid_list_input)
        self.assertEqual(data, self._valid_list_output)
