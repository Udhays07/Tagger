from django.shortcuts import render
from tagger.models import EntityType, Word


# def index(request):
#     return render(request, "tagger/index.html", {})

def index(request):
    entity_types = EntityType.objects.all()
    return render(request, "tagger/index.html", {'entity_types': entity_types})
