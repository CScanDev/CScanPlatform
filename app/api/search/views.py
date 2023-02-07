from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

import services
from parsers import models


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = (
            "id", "title", "link", "price", "diploma", "employment", "duration",
        )


class SearchView(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)

    @action(methods=["GET"], detail=False, url_path="search/(?P<query>[^/.]+)")
    def search(self, request: Request, query=None) -> Response:
        engine = services.SearchEngine()
        return Response(
            CourseSerializer(
                instance=engine.search(query),
                many=True
            ).data
        )
