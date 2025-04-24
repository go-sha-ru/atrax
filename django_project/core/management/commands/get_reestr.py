import csv

import requests
import urllib


from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import NumberingRegister


class Command(BaseCommand):
    help = """Загрузка реестра российской системы и плана нумерации
    https://opendata.digital.gov.ru/registry/numeric/downloads/"""
    download_urls = [
        "https://opendata.digital.gov.ru/downloads/ABC-3xx.csv",
        "https://opendata.digital.gov.ru/downloads/ABC-4xx.csv",
        "https://opendata.digital.gov.ru/downloads/ABC-8xx.csv",
        "https://opendata.digital.gov.ru/downloads/DEF-9xx.csv",
    ]

    def _setup(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }
        self.requests_session = requests.Session()
        self.requests_session.headers.update(headers)

    @staticmethod
    def _clear_registry():
        NumberingRegister.objects.all().delete()

    def _get_data(self, url):
        response = self.requests_session.get(url, timeout=10)
        data = list(line.decode('utf-8') for line in response.iter_lines())
        return data

    @staticmethod
    def _save(row: list) -> NumberingRegister:
        obj = NumberingRegister()
        obj.code = row[0]
        obj.start = row[1]
        obj.end = row[2]
        obj.capacity = row[3]
        obj.operator = row[4]
        obj.region = row[5]
        obj.territory = row[6]
        obj.inn = row[7]
        obj.save()
        return obj

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Старт"))
        self._clear_registry()
        self._setup()
        for url in self.download_urls:
            self.stdout.write(self.style.NOTICE(f"Загружается файл {url}"))
            try:
                data = self._get_data(url)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Произошла ошибка {url} Error: {e}"))
                continue
            csv_reader = csv.reader(data, delimiter=';')
            count = 0
            self.stdout.write(self.style.NOTICE(f"Сохранение в базе {url}"))
            for row in csv_reader:
                if count != 0:
                    self._save(row)
                count += 1
            self.stdout.write(self.style.NOTICE(f"Сохранение завершено {url}"))
        self.stdout.write(self.style.SUCCESS("Скрипт отработал"))
