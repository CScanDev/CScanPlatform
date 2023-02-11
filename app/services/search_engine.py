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

    def __init__(self):
        self.lemmatizer = pymorphy2.MorphAnalyzer()

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

    def build_index(self):
        index = defaultdict(list)
        courses = models.Course.objects.all()
        for course in courses:
            for token in self._tokenize(course.title):
                index[token].append(course.pk)

        with open(self.INDEX_PATH, "w", encoding="utf-8") as file:
            data = json.dumps(index, ensure_ascii=False)
            file.write(data)

    def _get_index(self) -> dict:
        with open(self.INDEX_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data

    def _tokenize(self, text: str) -> List[str]:
        return [
            self._lemmatize(word) for word in word_tokenize(text) if word not in stopwords.words("russian")
        ]

    def _lemmatize(self, word: str) -> str:
        return self.lemmatizer.parse(word)[0].normal_form
