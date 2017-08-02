"""
Provides XML rendering support.
"""
from __future__ import unicode_literals

from django.utils import six
from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.six import StringIO
from django.utils.encoding import force_text
from rest_framework.renderers import BaseRenderer
from xml.etree import ElementTree as ET


class XMLRenderer(BaseRenderer):
    """
    Renderer which serializes to XML.
    """

    media_type = 'application/xml'
    format = 'xml'
    charset = 'utf-8'
    item_tag_name = 'list-item'
    root_tag_name = 'root'
    override_item_tag_name = False

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders `data` into serialized XML.
        """
        if data is None:
            return ''

        stream = StringIO()

        xml = SimplerXMLGenerator(stream, self.charset)
        xml.startDocument()
        xml.startElement(self.root_tag_name, {})

        self._to_xml(xml, data)

        xml.endElement(self.root_tag_name)
        xml.endDocument()

        if self.override_item_tag_name:
            self._do_override_item_tag_name(stream)

        return stream.getvalue()

    def _do_override_item_tag_name(self, stream):
        root = ET.fromstring(stream.getvalue())
        for parent in root.findall('.//*list-item/..'):
            child_name = parent.tag[0:-1]
            for child in parent.getchildren():
                child.tag = child_name

        stream.truncate(0)
        stream.write('<?xml version="1.0" encoding="utf-8"?>\n')
        stream.write(str(ET.tostring(root)))

    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                xml.startElement(self.item_tag_name, {})
                self._to_xml(xml, item)
                xml.endElement(self.item_tag_name)

        elif isinstance(data, dict):
            for key, value in six.iteritems(data):
                xml.startElement(key, {})
                self._to_xml(xml, value)
                xml.endElement(key)

        elif data is None:
            # Don't output any value
            pass

        else:
            xml.characters(force_text(data))
