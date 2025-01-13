from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.TextField()
    work = models.CharField(max_length=100)

    def __str__(self):
        return self.name
