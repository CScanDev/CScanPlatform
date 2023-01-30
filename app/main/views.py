from typing import List

from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action

from main import services
from parsers import models


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ("title", "link", "price", "diploma", "employment", "duration",)


class MainView(viewsets.ViewSet):

    def list(self, request: Request) -> Response:
        queryset = models.Course.objects.filter(is_active=True)
        return Response(
            CourseSerializer(
                instance=queryset,
                many=True
            ).data
        )

    @action(methods=["GET"], detail=False, url_path="search/(?P<query>[^/.]+)")
    def search(self, request: Request, query=None) -> Response:
        engine = services.SearchEngine()
        return Response(
            CourseSerializer(
                instance=engine.search(query),
                many=True
            ).data
        )
