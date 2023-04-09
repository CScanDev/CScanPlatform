from typing import List, Union, Optional
from collections import defaultdict
import os
import json

from django.db.models import QuerySet
from django.conf import settings
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pymorphy2

from parsers import models


class SearchEngine:
    INDEX_FILE_NAME = "index.json"
    INDEX_PATH = os.path.join(settings.BASE_DIR, f"../{INDEX_FILE_NAME}")
    LEMMATIZER = pymorphy2.MorphAnalyzer()

    def search(self, query: str) -> Optional[Union[QuerySet, List[models.Course]]]:
        try:
            index = self._get_index()
        except FileNotFoundError:
            print("No index file")
            return []

        ids = []
        for word in self._tokenize(query):
            ids.extend(index.get(word, []))
        return models.Course.objects.filter(id__in=ids)

    @classmethod
    def build_index(cls):
        index = defaultdict(list)
        courses = models.Course.objects.all()
        for course in courses:
            for token in cls._tokenize(course.title):
                index[token].append(course.pk)

        with open(cls.INDEX_PATH, "w", encoding="utf-8") as file:
            data = json.dumps(index, ensure_ascii=False)
            file.write(data)

    def _get_index(self) -> dict:
        with open(self.INDEX_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data

    @classmethod
    def _tokenize(cls, text: str) -> List[str]:
        return [
            cls._lemmatize(word) for word in word_tokenize(text) if word not in stopwords.words("russian")
        ]

    @classmethod
    def _lemmatize(cls, word: str) -> str:
        return cls.LEMMATIZER.parse(word)[0].normal_form
