from django.db import models, transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Sentence(models.Model):
    text = models.TextField(unique=True)
    order = models.IntegerField(unique=True, blank=True, null=True)  # Added order field to keep track of sentence order

    def __str__(self):
        return self.text
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
    
@receiver(pre_save, sender=Sentence)
def set_order(sender, instance, **kwargs):
    if instance.order is None:
        # Ensure atomicity when assigning order
        with transaction.atomic():
            # Get the highest `order` value and assign the next value
            max_order = Sentence.objects.aggregate(models.Max('order'))['order__max']
            instance.order = (max_order or 0) + 1
