from typing import List, Union
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
    index_file_name = "index.json"
    index_path = os.path.join(settings.BASE_DIR, f"../{index_file_name}")

    def __init__(self):
        self.lemmatizer = pymorphy2.MorphAnalyzer()

    def search(self, query: str) -> Union[QuerySet, List[models.Course]]:
        index = self._get_index()
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

        with open(self.index_path, "w") as file:
            data = json.dumps(index, ensure_ascii=False)
            file.write(data)

    def _get_index(self) -> dict:
        with open(self.index_path, "r") as file:
            data = json.load(file)
            return data

    def _tokenize(self, text: str) -> List[str]:
        return [
            self._lemmatize(word) for word in word_tokenize(text) if word not in stopwords.words("russian")
        ]

    def _lemmatize(self, word: str) -> str:
        return self.lemmatizer.parse(word)[0].normal_form
