# Renderers

## Setting the renderers

The default set of renderers may be set globally, using the `DEFAULT_RENDERER_CLASSES` setting.  For example, the following settings would use `XML` as the main media type and also include the self describing API.

    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework_xml.renderers.XMLRenderer',
        )
    }

You can also set the renderers used for an individual view, or viewset,
using the `APIView` class based views.

    from django.contrib.auth.models import User
    from rest_framework.response import Response
    from rest_framework.views import APIView
    from rest_framework_xml.renderers import XMLRenderer

    class UserCountView(APIView):
        """
        A view that returns the count of active users in XML.
        """
        renderer_classes = (XMLRenderer,)

        def get(self, request, format=None):
            user_count = User.objects.filter(active=True).count()
            content = {'user_count': user_count}
            return Response(content)

Or, if you're using the `@api_view` decorator with function based views.

    @api_view(['GET'])
    @renderer_classes((XMLRenderer,))
    def user_count_view(request, format=None):
        """
        A view that returns the count of active users in XML.
        """
        user_count = User.objects.filter(active=True).count()
        content = {'user_count': user_count}
        return Response(content)

---

# API Reference

## XMLRenderer

Renders REST framework's default style of `XML` response content.

Note that the `XML` markup language is used typically used as the base language for more strictly defined domain-specific languages, such as `RSS`, `Atom`, and `XHTML`.

If you are considering using `XML` for your API, you may want to consider implementing a custom renderer and parser for your specific requirements, and using an existing domain-specific media-type, or creating your own custom XML-based media-type.

**.media_type**: `application/xml`

**.format**: `'.xml'`

**.charset**: `utf-8`
