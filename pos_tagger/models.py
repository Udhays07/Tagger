from django.db import models, transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Sentence Model
class Sentence(models.Model):
    text = models.TextField()
    order = models.IntegerField(unique=True, blank=True, null=True) 

    def __str__(self):
        return self.text

# Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# POS Model - Link each word with a tag and a sentence
class POS(models.Model):
    word = models.CharField(max_length=100)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, related_name='poss')
    sentence = models.ForeignKey('Sentence', on_delete=models.CASCADE, related_name='poss')

    def __str__(self):
        return f"{self.word} - {self.tag.name} in {self.sentence.text}"

# NounChunk Model - Represent the chunk of words identified as a noun phrase
class NounChunk(models.Model):
    sentence = models.ForeignKey('Sentence', on_delete=models.CASCADE, related_name='noun_chunks')
    words = models.ManyToManyField('POS', related_name='noun_chunks')
    chunk_text = models.CharField(max_length=500)  # Store the text of the noun chunk

    def __str__(self):
        return self.chunk_text

@receiver(pre_save, sender=Sentence)
def set_order(sender, instance, **kwargs):
    if instance.order is None:
        # Ensure atomicity when assigning order
        with transaction.atomic():
            # Get the highest `order` value and assign the next value
            max_order = Sentence.objects.aggregate(models.Max('order'))['order__max']
            instance.order = (max_order or 0) + 1
