from django.db import models

class Sentence(models.Model):
    sentence_text = models.TextField()

    def __str__(self):
        return f"Sentence {self.id}: {self.sentence_text}"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class POSTag(models.Model):
    word = models.CharField(max_length=255)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, related_name='words')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tagged_words')

    def __str__(self):
        return f"{self.sentence.id} - {self.word} : {self.tag.name}"

