from django.contrib import admin
from .models import Sentence,POSTag,Tag

admin.site.register(Sentence)
admin.site.register(POSTag)
from postagger.models import Tag

predefined_tags = [ 'Noun','Compound Noun','Proper Noun','Cardinals','Pronoun','Pronoun Interrogative','Pronoun Indefinite','Adjective',
'Adverb','VNF Adjective','VNF Adverb','Verbal Gerund','Verb Finite','Verb Auxiliary','Verb Infinite','Conjunction','Quantifiers','PostPositions',
'Determiners','Intensifier','Echo Words','Emphasis','Comma','Dot','Question Marks',
'Reduplication Words'
]

for tag_name in predefined_tags:
    Tag.objects.get_or_create(name=tag_name)
admin.site.register(Tag)


