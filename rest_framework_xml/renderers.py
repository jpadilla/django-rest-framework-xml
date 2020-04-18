"""
Provides XML rendering support.
"""
from io import StringIO

from django.utils.encoding import force_str
from django.utils.xmlutils import SimplerXMLGenerator
from rest_framework.renderers import BaseRenderer


class XMLRenderer(BaseRenderer):
    """
    Renderer which serializes to XML.
    """

    media_type = 'application/xml'
    format = 'xml'
    charset = 'utf-8'
    item_tag_name = 'list-item'
    root_tag_name = 'root'

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
        return stream.getvalue()

    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                xml.startElement(self.item_tag_name, {})
                self._to_xml(xml, item)
                xml.endElement(self.item_tag_name)

        elif isinstance(data, dict):
            for key, value in data.items():
                xml.startElement(key, {})
                self._to_xml(xml, value)
                xml.endElement(key)

        elif data is None:
            # Don't output any value
            pass

        else:
            xml.characters(force_str(data))


class SOAPRenderer(BaseRenderer):
    """
    Renderer which serialize to SOAP Envelope
    """
    media_type = 'application/xml'
    format = 'xml'
    charset = 'utf-8'

    soap_tag = 'SOAP-ENV'
    service_endpoint = 'http://dummyservice.com/endpoint'
    service_name = 'dummyService'

    schema_attrs = {
        'xmlns:%s' % soap_tag: 'http://schemas.xmlsoap.org/soap/envelope/',
        'xmlns:%s' % service_name: '%s' % service_endpoint
    }

    envelope_tag_name = '%s:Envelope' % soap_tag
    header_tag_name = '%s:Header' % soap_tag
    body_tag_name = '%s:Body' % soap_tag
    response_tag_name = '%s:Response' % service_name

    @classmethod
    def set_schema_attrs(cls, soap_tag, service_endpoint, service_name):
        cls.envelope_tag_name = '%s:Envelope' % soap_tag
        cls.header_tag_name = '%s:Header' % soap_tag
        cls.body_tag_name = '%s:Body' % soap_tag
        cls.response_tag_name = '%s:Response' % service_name

        cls.schema_attrs = {
            'xmlns:%s' % soap_tag: 'http://schemas.xmlsoap.org/soap/envelope/',
            'xmlns:%s' % service_name: '%s' % service_endpoint
        }

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders `data` into serialized SOAP Envelope.
        """
        if not data:
            return ''

        stream = StringIO()

        xml = SimplerXMLGenerator(stream, self.charset)
        xml.startDocument()

        xml.startElement(self.envelope_tag_name, self.schema_attrs)
        xml.addQuickElement(self.header_tag_name)
        xml.startElement(self.body_tag_name, {})
        xml.startElement(self.response_tag_name, {})

        self._to_xml(xml, data)

        xml.endElement(self.response_tag_name)
        xml.endElement(self.body_tag_name)
        xml.endElement(self.envelope_tag_name)

        return stream.getvalue()

    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                self._to_xml(xml, item)

        elif isinstance(data, dict):
            for key, value in data.items():
                xml.startElement(key, {})
                self._to_xml(xml, value)
                xml.endElement(key)

        elif data is None:
            # Don't output any value
            pass

        else:
            xml.characters(force_str(data))