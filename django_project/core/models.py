from django.db import models


class NumberingRegister(models.Model):
    code = models.IntegerField(verbose_name="ABC / DEF")
    start = models.BigIntegerField(verbose_name="От")
    end = models.BigIntegerField(verbose_name="До")
    capacity = models.IntegerField(verbose_name="Ёмкость")
    operator = models.CharField(max_length=255, verbose_name="Оператор")
    region = models.CharField(max_length=255, verbose_name="Регион")
    territory = models.CharField(max_length=255, verbose_name="Территория ГАР")
    inn = models.CharField(max_length=255, verbose_name="ИНН")

    def __str__(self):
        return str(f"{self.operator}: 7({self.code}) {self.start} - {self.end}")

    class Meta:
        verbose_name = "Реестр российской системы и плана нумерации"
        verbose_name_plural = "Реестр российской системы и плана нумерации"
