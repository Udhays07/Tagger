from django.contrib import admin
# from .models import EntityType, Word
# from .models import tagger
from .models import NER, Tag, Sentence

admin.site.register(NER)
admin.site.register(Tag)
admin.site.register(Sentence)
# admin.site.register(EntityType)
# admin.site.register(Word)