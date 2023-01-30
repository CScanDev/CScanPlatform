from decimal import Decimal

from django.db import models


class Source(models.Model):
    name = models.CharField("Name", max_length=64, unique=True)
    link = models.URLField("Link", max_length=256)
    is_active = models.BooleanField("Is active?", default=False)

    def __str__(self) -> str:
        return f"{self.name} - {self.link}"


class Config(models.Model):
    source = models.ForeignKey("Source", on_delete=models.SET_NULL, related_name="config", null=True)
    content_link = models.URLField("Content link", max_length=256, default="")
    is_active = models.BooleanField("Is active?", default=False)
    is_multiple_pages = models.BooleanField("Is multiple pages?", default=False)

    def __str__(self) -> str:
        return f"{self.source.name} Config"


class Tag(models.Model):
    MAIN = "main"
    TITLE = "title"
    LINK = "link"
    PRICE = "price"
    DIPLOMA = "diploma"
    EMPLOYMENT = "employment"
    DURATION = "duration"
    NEXT_PAGE = "next_page"
    TAG_CATEGORIES = (
        MAIN,
        TITLE,
        LINK,
        PRICE,
        DIPLOMA,
        EMPLOYMENT,
        DURATION,
        NEXT_PAGE,
    )
    TAG_CATEGORIES_CHOICES = (
        (MAIN, "Main"),
        (TITLE, "Title"),
        (LINK, "Link"),
        (PRICE, "Price"),
        (DIPLOMA, "Diploma"),
        (EMPLOYMENT, "Employment"),
        (DURATION, "Duration"),
        (NEXT_PAGE, "Next page button"),
    )
    config = models.ForeignKey("Config", on_delete=models.CASCADE, related_name="tags")
    name = models.CharField("Tag name", max_length=128)
    class_name = models.CharField("Tag class", max_length=128)
    category = models.CharField(max_length=64, choices=TAG_CATEGORIES_CHOICES)
    data_pointer = models.CharField(max_length=64, default="", blank=True)
    tag_order_number = models.PositiveIntegerField("Tag order number", default=1)

    def __str__(self) -> str:
        return f"{self.config} {self.category}"


class Course(models.Model):
    title = models.CharField("Title", max_length=255)
    link = models.CharField("Link to buy", max_length=255, unique=True)
    price = models.DecimalField("Price", default=Decimal(0), decimal_places=2, max_digits=10)
    diploma = models.BooleanField("Diploma?", default=False)
    employment = models.BooleanField("Is employment guaranteed?", default=False)
    duration = models.CharField("Duration", max_length=255, blank=True)

    source = models.ForeignKey("Source", on_delete=models.PROTECT, related_name="courses")

    created = models.DateTimeField("Created", auto_now_add=True)
    updated = models.DateTimeField("Last update", auto_now=True)
    is_active = models.BooleanField("Is active?", default=False)




