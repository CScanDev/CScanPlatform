from typing import Union, List

from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action

from parsers import models
from services import CourseService
from api.base import BaseViewSet


Courses = Union[List[models.Course], QuerySet]


class CourseSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="source.name")

    class Meta:
        model = models.Course
        fields = [
            "title",
            "link",
            "price",
            "diploma",
            "employment",
            "duration",
            "source",
        ]


class AddCourseSerializer(serializers.Serializer):
    course_svc = CourseService()

    title = serializers.CharField()
    link = serializers.CharField()
    price = serializers.CharField()
    diploma = serializers.BooleanField()
    employment = serializers.BooleanField()
    duration = serializers.CharField()
    source = serializers.CharField()

    def validate_source(self, value: str):
        try:
            source = self.course_svc.get_source(value)
            return source
        except models.Source.DoesNotExist:
            raise serializers.ValidationError("Source is not found")

    def create(self, validated_data):
        return self.course_svc.create_course(
            validated_data["title"],
            validated_data["link"],
            validated_data["price"],
            validated_data["diploma"],
            validated_data["employment"],
            validated_data["duration"],
            validated_data["source"],
        )


class DashboardView(BaseViewSet):
    course_svc = CourseService()

    @action(methods=["GET"], detail=False)
    def get_user_courses(self, request: Request) -> Response:
        return Response(
            CourseSerializer(
                instance=self.course_svc.get_user_courses(request.user),
                many=True,
                context={"request": request},
            ).data
        )

    @action(methods=["POST"], detail=False, serializer_class=AddCourseSerializer)
    def add_course(self, request: Request):
        serializer = AddCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course: models.Course = serializer.save()
        return Response(
            CourseSerializer(
                instance=course,
                context={"request": request},
            ).data
        )
