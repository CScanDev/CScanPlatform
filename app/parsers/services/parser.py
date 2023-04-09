import re
import sys
import time
from decimal import Decimal
from random import randint
from typing import List, Optional, Any
from contextlib import contextmanager
from dataclasses import dataclass

from django.conf import settings

from bs4 import BeautifulSoup
from bs4.element import Tag as PageTag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from parsers.services.exceptions import *
from parsers import models
from services import SearchEngine


HTML = str


@dataclass(init=False)
class Course:
    title: str = None
    link: str = None
    price: Decimal = None
    diploma: bool = None
    employment: bool = None
    duration: str = None


@contextmanager
def browser_manager():
    browser = ChromeWebDriver().get_browser()
    try:
        yield browser
    except Exception as exc:
        raise CantGetPage from exc
    finally:
        browser.quit()


class ChromeWebDriver:

    def __init__(self):
        self.driver_location = None
        self.binary_location = None
        self._set_path_parameters()

    def _set_path_parameters(self):
        if "linux" in sys.platform:
            self.driver_location = "/usr/local/bin/chromedriver"
            self.binary_location = "/home/denis/chrome/chrome"
        else:
            self.driver_location = "../web_drivers/windows/chromedriver.exe"

    def get_browser(self) -> webdriver.Chrome:
        options = Options()
        options.headless = True
        if self.binary_location:
            options.binary_location = self.binary_location

        return webdriver.Chrome(
            executable_path=self.driver_location,
            options=options
        )


class BaseParser:
    def __init__(self, source: models.Source):
        self.source = source
        self.config = None
        self._set_config()

    def _set_config(self):
        config = self.source.config.filter(is_active=True).first()
        if not config:
            raise models.Config.DoesNotExist
        self.config = config

    @property
    def main_tag(self) -> models.Tag:
        return self.config.tags.get(category=models.Tag.MAIN)

    @property
    def data_tags(self) -> List[models.Tag]:
        return self.config.tags.exclude(category=models.Tag.MAIN).all()


class DataExtractor:

    def _get_value_by_tag(
            self, course: PageTag, tag: models.Tag
    ) -> Optional[Any]:
        try:
            page_tags = course.find_all(tag.name, class_=tag.class_name)
            value = self._get_value(tag, page_tags)
            return value
        except (AttributeError, IndexError):
            return None

    def _get_value(self, tag: models.Tag, page_tags: List[PageTag]):
        block = page_tags[tag.tag_order_number - 1]
        value = block.text

        if tag.data_pointer == "href":
            value = block.get("href")

        return self._process_value(value, tag.category)

    @staticmethod
    def _process_value(value: str, tag_category: str):
        match tag_category:
            case models.Tag.PRICE:
                match = re.match(r"(\d+[,|.]*\d{2})", value.replace(" ", ""))
                return match and match.group(1) or 0
            case models.Tag.DIPLOMA:
                return bool(value)
            case models.Tag.LINK:
                if "roistat_visit" in value:
                    return value.split("?")[0]
                return value
            case _:
                return value


class Parser(BaseParser, DataExtractor):

    def __init__(self, source: models.Source):
        super().__init__(source)

    def parse(self, update_index: bool = False):
        page: HTML = self._get_page(self.config.content_link)
        courses: List[PageTag] = self._extract_courses_from_page(page)
        courses: List[Course] = self._parse_course_data(courses)
        self._save_courses(courses)
        if update_index:
            SearchEngine.build_index()

    @classmethod
    def _get_page(cls, link: str) -> Optional[HTML]:
        with browser_manager() as browser:
            browser.get(link)
            time.sleep(randint(2, 4))  # Wait for page to fully load
            html = browser.page_source
            return html

    def _extract_courses_from_page(self, page: HTML) -> List[PageTag]:
        soup = BeautifulSoup(page, settings.HTML_PARSER)
        courses = soup.find_all(self.main_tag.name,
                                class_=self.main_tag.class_name)
        return courses

    def _parse_course_data(self, courses: List[PageTag]) -> List[Course]:
        result = []
        for course in courses:
            _course = Course()
            for tag in self.data_tags:
                if getattr(_course, tag.category):
                    continue
                value = self._get_value_by_tag(course, tag)
                setattr(_course, tag.category, value)
            result.append(_course)
        return result

    def _save_courses(self, courses: List[Course]):
        for course in courses:
            models.Course.objects.update_or_create(
                title=course.title,
                price=course.price,
                diploma=course.diploma,
                duration=course.duration,
                is_active=True,
                defaults={
                    "link": course.link,
                    "source": self.source,
                },
            )