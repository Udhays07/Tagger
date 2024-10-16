from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import NER, Tag
import json

def index(request):
    ner_entries = list(NER.objects.values('word', 'tag__name'))  # Fetch tag name directly

    if request.method == 'POST':
        # Handle saving of tagged words
        try:
            data = json.loads(request.body)
            tagged_words = data.get('tagged_words', [])

            # Save each tagged word to the database
            for item in tagged_words:
                word = item['word']
                tag_name = item['tag']
                
                # Get or create the tag
                tag, created = Tag.objects.get_or_create(name=tag_name)
                
                # Create the NER entry
                NER.objects.create(word=word, tag=tag)

            return JsonResponse({'status': 'success'})  # Return a success response
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    return render(request, 'tagger/index.html', {'ner_entries': json.dumps(ner_entries)})  # Pass the NER data to the template

def save_ner_entry(request):
    if request.method == "POST":
        word = request.POST.get('word')
        tag_name = request.POST.get('tag')
        if word and tag_name:
            tag, created = Tag.objects.get_or_create(name=tag_name)  # Get or create the tag
            NER.objects.create(word=word, tag=tag)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid data'})

@csrf_exempt
def fetch_existing_tags(request):
    if request.method == "POST":
        data = json.loads(request.body)
        words = data.get('words', [])
        tags = {}

        # Fetch tags from the database for the given words
        for word in words:
            try:
                ner_entry = NER.objects.get(word=word)
                tags[word] = ner_entry.tag.name  # Return tag name
            except NER.DoesNotExist:
                continue

        return JsonResponse(tags)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
