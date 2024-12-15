from django.contrib import admin
from .models import EntityType, Word
# from .models import tagger

# admin.site.register(tagger)
admin.site.register(EntityType)
admin.site.register(Word)