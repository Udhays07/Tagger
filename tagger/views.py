from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction
from .models import NER, Tag, Sentence
import json
from django.http import JsonResponse, HttpResponse
import logging

# Set up logging
logger = logging.getLogger(__name__)

@csrf_exempt
def save_sentences(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sentences = data.get('sentences', [])

            # Save each sentence to the database
            for sentence_text in sentences:
                Sentence.objects.create(text=sentence_text)

            return JsonResponse({'message': 'Sentences saved successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def save_tagged_words(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tagged_words = data.get('tagged_words')

            if not tagged_words:
                return JsonResponse({'error': 'No tagged words received'}, status=400)

            with transaction.atomic():  
                for tagged_word in tagged_words:
                    word = tagged_word.get('word')
                    tag_name = tagged_word.get('tag')
                    sentence_text = tagged_word.get('sentence')

                    if not word or not tag_name or not sentence_text:
                        return JsonResponse({'error': 'Invalid tagged word data'}, status=400)

                    # Get the Sentence object, creating it if it doesn't exist
                    sentence, created = Sentence.objects.get_or_create(text=sentence_text)

                    # Get the Tag object, creating it if it doesn't exist
                    tag, created = Tag.objects.get_or_create(name=tag_name)

                    # Create the NER entry
                    NER.objects.create(word=word, tag=tag, sentence=sentence)

            return JsonResponse({'message': 'Tagged words saved successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': 'Failed to save tagged words', 'details': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
def index(request):
    ner_entries = list(NER.objects.values('word', 'tag__name'))  # Fetch tag name directly
    return render(request, 'tagger/index.html', {'ner_entries': json.dumps(ner_entries)})

def fetch_tag_table(request):
    tag_entries = NER.objects.select_related('tag').values('word', 'tag__name')
    data = [{'word': entry['word'], 'tag': entry['tag__name']} for entry in tag_entries]
    return JsonResponse(data, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def update_tag(request):
    try:
        data = json.loads(request.body)
        word = data.get("word")
        new_tag_name = data.get("new_tag")
        
        # Find the tag and update it
        ner_instance = NER.objects.get(word=word)
        tag, created = Tag.objects.get_or_create(name=new_tag_name)
        ner_instance.tag = tag
        ner_instance.save()
        
        return JsonResponse({"status": "success", "message": "Tag updated successfully."}, status=200)
    except NER.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Word not found."}, status=404)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_tag(request, id):
    try:
        ner_instance = NER.objects.get(id=id)
        ner_instance.delete()
        return JsonResponse({"status": "success", "message": "Tag deleted successfully."}, status=204)
    except NER.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Tag not found."}, status=404)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)