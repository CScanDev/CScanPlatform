from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


import services
from parsers import models


query = openapi.Parameter(
    "query", openapi.IN_QUERY,
    required=True, type=openapi.TYPE_STRING
)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = (
            "id", "title", "link", "price", "diploma", "employment", "duration",
        )


class SearchView(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(manual_parameters=[query])
    @action(methods=["GET"], detail=False)
    def search(self, request: Request) -> Response:
        engine = services.SearchEngine()
        return Response(
            CourseSerializer(
                instance=engine.search(
                    request.GET.get(query.name, None)
                ),
                many=True
            ).data
        )


class TestView(viewsets.ViewSet):
    def list(self, request):
        return Response("Test")
