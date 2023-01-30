from typing import List, Union

from django.db.models import QuerySet
from django.contrib import admin

from parsers import models
from parsers.services import Parser


@admin.action(description="Start parsing...")
def run_parser(modeladmin, request, queryset: Union[QuerySet, List[models.Source]]):
    for source in queryset:
        parser = Parser(source)
        parser.parse()


class SourceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "link",
        "is_active",
    )
    actions = [run_parser, ]


class ConfigAdmin(admin.ModelAdmin):
    list_display = (
        "source",
        "is_active",
        "is_multiple_pages",
    )


class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "source", "updated", "is_active",)
    list_editable = ("is_active",)


admin.site.register(models.Source, SourceAdmin)
admin.site.register(models.Config, ConfigAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Course, CourseAdmin)


