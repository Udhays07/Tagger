from django.contrib import admin
from .models import POS, Tag, Sentence, NounChunk

admin.site.register(POS)
admin.site.register(Tag)
admin.site.register(Sentence)
admin.site.register(NounChunk)
