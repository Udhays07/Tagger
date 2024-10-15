# from django.db import models

# class tagger(models.Model):
#     word = models.CharField(max_length=100)
#     entity = models.CharField(max_length=100)

from django.db import models

class EntityType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Word(models.Model):
    text = models.CharField(max_length=100)
    entity_type = models.ForeignKey(EntityType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text} - {self.entity_type.name}"
