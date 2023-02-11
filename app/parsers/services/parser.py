import time
from typing import List, Optional
from random import randint
import re

from django.conf import settings

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from bs4.element import Tag as _Tag

from parsers.services.exceptions import *
from parsers import models


HTML = str


class Parser:

    def __init__(self, source: models.Source):
        self.source = source
        self.config = None

    def parse(self):
        self._set_config()
        page = self._get_page()
        self._page2courses(page)

    def _set_config(self):
        config = self.source.config.filter(is_active=True).first()
        if not config:
            raise models.Config.DoesNotExist
        self.config = config

    def _get_page(self) -> Optional[HTML]:
        options = Options()
        options.headless = True
        browser = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        try:
            browser.get(self.config.content_link)
            time.sleep(randint(3, 6))
            html = browser.page_source
        except Exception as exc:
            raise CantGetPage from exc
        finally:
            browser.quit()
        return html

    def _page2courses(self, page: HTML):
        soup = BeautifulSoup(page, settings.HTML_PARSER)
        main_tag = self.config.tags.get(category=models.Tag.MAIN)
        courses_containers = soup.find_all(main_tag.name, class_=main_tag.class_name)

        for course in courses_containers:
            data = {}
            for tag in self.config.tags.exclude(category=models.Tag.MAIN).all():
                if data.get(tag.category, None):
                    continue
                data = self._parse_by_tag(course, tag, data)
            self._save_course(data)

    def _parse_by_tag(self, course: _Tag, tag: models.Tag, data: dict) -> dict:
        try:
            block_list = course.find_all(tag.name, class_=tag.class_name)
            value = self._get_value(tag, block_list)
            data[tag.category] = self._process_value(value, tag.category)
        except (AttributeError, IndexError):
            pass
        return data

    def _get_value(self, tag: models.Tag, block_list: List[_Tag]):
        block = block_list[tag.tag_order_number - 1]
        if tag.data_pointer == "href":
            return block.get("href")
        else:
            return block.text

    def _process_value(self, value, tag_category: str):
        match tag_category:
            case models.Tag.PRICE:
                match = re.match(r"(\d+[,|.]*\d{2})", value.replace(" ", ""))
                return match and match.group(1) or 0
            case models.Tag.DIPLOMA:
                return bool(value)
            case _:
                return value

    def _save_course(self, data: dict):
        models.Course.objects.update_or_create(
            title=data["title"],
            price=data["price"],
            diploma=data["diploma"],
            duration=data["duration"],
            is_active=True,
            defaults={
                "link": data["link"],
                "source": self.source,
            },
        )