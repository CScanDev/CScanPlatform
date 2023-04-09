from typing import Union, List, Optional

from django.db.models import QuerySet

from parsers import models

Courses = Union[List[models.Course], QuerySet]


class CourseService:

    @classmethod
    def get_user_courses(cls, user) -> Courses:
        source = models.Source.objects.get(manager=user)
        return source.courses.filter(is_active=True)

    @classmethod
    def create_course(
            cls,
            title,
            link,
            price,
            diploma,
            employment,
            duration,
            source,
    ) -> Optional[models.Course]:
        return models.Course.objects.create(
            title=title,
            link=link,
            price=price,
            diploma=diploma,
            employment=employment,
            duration=duration,
            source=source,
            is_active=True,
        )

    @classmethod
    def get_source(cls, value: str) -> Optional[models.Source]:
        return models.Source.objects.get(pk=value)
