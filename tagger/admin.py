from django.contrib import admin
from .models import NER, Tag, Sentence

admin.site.register(NER)
admin.site.register(Tag)
admin.site.register(Sentence)
