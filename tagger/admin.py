from django.contrib import admin
<<<<<<< HEAD
=======
# from .models import EntityType, Word
# from .models import tagger
>>>>>>> 155ac80366fd9f0aea0023d87e440b36dca5cdec
from .models import NER, Tag, Sentence

admin.site.register(NER)
admin.site.register(Tag)
admin.site.register(Sentence)
<<<<<<< HEAD
=======
# admin.site.register(EntityType)
# admin.site.register(Word)
>>>>>>> 155ac80366fd9f0aea0023d87e440b36dca5cdec
