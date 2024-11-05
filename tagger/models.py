from django.db import models

class Sentence(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class NER(models.Model):
    word = models.CharField(max_length=100)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, related_name='ners')
    sentence = models.ForeignKey('Sentence', on_delete=models.CASCADE, related_name='ners')

    def __str__(self):
        return f"{self.word} - {self.tag.name} in {self.sentence.text}"