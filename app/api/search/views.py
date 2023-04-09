from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions

import services
from parsers import models
from api.base import BaseViewSet


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = (
            "id", "title", "link", "price", "diploma", "employment", "duration",
        )


class SearchView(BaseViewSet):
    permission_classes = (permissions.AllowAny,)

    @action(methods=["GET"], detail=False, url_path="search/(?P<query>[^/.]+)")
    def search(self, request: Request, query=None) -> Response:
        engine = services.SearchEngine()
        return Response(
            CourseSerializer(
                instance=engine.search(query),
                many=True
            ).data
        )
