from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction
from .models import NER, Tag, Sentence
import json

# This view saves the sentences, splits the text, and stores them in the database
@csrf_exempt
def ner_save_sentences(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sentences = data.get('sentences', [])

            # Save each sentence to the database and store the sentence texts in session
            saved_sentences = []
            for sentence_text in sentences:
                # Create a new Sentence object and set its text
                sentence = Sentence(text=sentence_text)
                sentence.save()  # This will trigger the pre_save signal and auto-assign the `order` field
                
                saved_sentences.append(sentence.id)  # Store the sentence ID in session

            # Store the sentence IDs in the session for use in main1.html
            request.session['saved_sentences'] = saved_sentences

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

# This is the index view that renders the first page, displaying the NER entries
# def index(request):
#     # Fetch existing NER entries for display
#     ner_entries = list(NER.objects.values('word', 'tag__name'))  # Fetch tag name directly
#     return render(request, 'tagger/index.html', {'ner_entries': json.dumps(ner_entries)})


# This view handles displaying sentences one by one in order
# Inside the main1 view
def main1(request):
    # Get the saved sentence IDs from the session
    saved_sentence_ids = request.session.get('saved_sentences', [])

    if not saved_sentence_ids:
        sentences = []  # If no sentences are saved in the session
    else:
        # Fetch the sentences ordered by the 'order' field
        sentences = Sentence.objects.filter(id__in=saved_sentence_ids).order_by('order')

    # Retrieve the current sentence index from the session (default is 0)
    sentence_index = request.session.get('sentence_index', 0)

    if sentence_index >= len(sentences):
        sentence_index = 0  # Loop back to the first sentence if the index exceeds the length

    # Get the current sentence based on the sentence_index
    current_sentence = sentences[sentence_index] if sentences else None

    # Pass the current sentence and the total number of sentences to the template
    context = {
        'sentence': current_sentence.text if current_sentence else '',
        'sentence_index': sentence_index,
        'total_sentences': len(sentences),
        'sentences': json.dumps([sentence.text for sentence in sentences]),  # Ensure proper JSON serialization
    }

    return render(request, 'tagger/main1.html', context)


def update_sentence_index(request):
    print("Received request to update sentence index")  # Add this line
    if request.method == 'POST':
        data = json.loads(request.body)
        sentence_index = data.get('index', 0)
        request.session['sentence_index'] = sentence_index
        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)

# This is the main index page view
def tagger_index(request):
    return render(request, 'tagger/index.html')
