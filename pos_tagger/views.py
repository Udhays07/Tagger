from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction
from .models import POS, Tag, Sentence, NounChunk
import json

@csrf_exempt
def pos_save_sentences(request):
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
            noun_chunks = data.get('noun_chunks', [])  # Add noun chunks info here

            if not tagged_words:
                return JsonResponse({'error': 'No tagged words received'}, status=400)

            with transaction.atomic():
                for tagged_word in tagged_words:
                    word = tagged_word.get('word')
                    tag_name = tagged_word.get('tag')
                    sentence_text = tagged_word.get('sentence')

                    if not word or not tag_name or not sentence_text:
                        return JsonResponse({'error': 'Invalid tagged word data'}, status=400)

                    # Get or create the Sentence object
                    sentence, created = Sentence.objects.get_or_create(text=sentence_text)

                    # Get or create the Tag object
                    tag, created = Tag.objects.get_or_create(name=tag_name)

                    # Create the POS entry
                    POS.objects.create(word=word, tag=tag, sentence=sentence)

                # Handle the creation of noun chunks
                for chunk in noun_chunks:
                    sentence_text = chunk.get('sentence')
                    chunk_words = chunk.get('words')  # List of word IDs that form the noun chunk
                    
                    if not sentence_text or not chunk_words:
                        continue  # Skip invalid chunks

                    # Get the sentence object for the noun chunk
                    sentence = Sentence.objects.get(text=sentence_text)

                    # Fetch POS objects based on the word IDs
                    pos_objects = POS.objects.filter(id__in=chunk_words)

                    # Create a new noun chunk
                    noun_chunk_text = " ".join([pos.word for pos in pos_objects])
                    noun_chunk = NounChunk.objects.create(
                        sentence=sentence,
                        chunk_text=noun_chunk_text
                    )

                    # Link the POS words to the noun chunk
                    noun_chunk.words.set(pos_objects)

            return JsonResponse({'message': 'Tagged words and noun chunks saved successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': 'Failed to save tagged words or noun chunks', 'details': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def index(request):
    pos_entries = list(POS.objects.values('word', 'tag'))  # Fetch tag name directly
    return render(request, 'pos_tagger/index.html', {'pos_entries': json.dumps(pos_entries)})

def fetch_tag_table(request):
    tag_entries = POS.objects.select_related('tag').values('word', 'tag__name')
    data = [{'word': entry['word'], 'tag': entry['tag__name']} for entry in tag_entries]
    return JsonResponse(data, safe=False)

# def main(request):
#     # Fetch all saved sentences to display them on index1
#     sentences = Sentence.objects.all()
#     return render(request, 'pos_tagger/main.html', {'sentences': sentences})

def main(request):
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

    # Fetch the noun chunks for the current sentence
    noun_chunks = NounChunk.objects.filter(sentence=current_sentence) if current_sentence else []

    # Pass the current sentence, noun chunks, and other context data to the template
    context = {
        'sentence': current_sentence.text if current_sentence else '',
        'sentence_index': sentence_index,
        'total_sentences': len(sentences),
        'sentences': json.dumps([sentence.text for sentence in sentences]),  # Ensure proper JSON serialization
        'noun_chunks': noun_chunks  # Pass noun chunks to the template
    }

    return render(request, 'pos_tagger/main.html', context)

def update_sentence_index(request):
    print("Received request to update sentence index")  # Add this line
    if request.method == 'POST':
        data = json.loads(request.body)
        sentence_index = data.get('index', 0)
        request.session['sentence_index'] = sentence_index
        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)

def pos_tagger_index(request):
    return render(request, 'pos_tagger/index.html')

# def home(request):
#     # You can choose to redirect to one of the apps, for example:
#     return redirect('tagger_index')