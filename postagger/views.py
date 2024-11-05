from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import POSTag, Sentence, Tag

@csrf_exempt
def save_sentence(request):
    if request.method == 'POST':
        sentence_text = request.POST.get('sentence')
        sentence_obj, created = Sentence.objects.get_or_create(sentence_text=sentence_text)
        
        return JsonResponse({'status': 'success', 'sentence_id': sentence_obj.id})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def save_pos_tags(request):
    if request.method == 'POST':
        sentence_id = request.POST.get('sentence_id')
        taggedWords = request.POST.getlist('taggedWords[]')

        # Retrieve the sentence object based on ID
        try:
            sentence = Sentence.objects.get(id=sentence_id)
            print(f"Sentence found: {sentence}")
        except Sentence.DoesNotExist:
            print("Error: Sentence does not exist.")
            return JsonResponse({'status': 'error', 'message': 'Sentence not found'}, status=400)

        for item in taggedWords:
            word, separator, tag = item.partition(':')
            if separator:
                word = word.strip()
                tag = tag.strip()
                originalIndex = originalIndex.strip()
                print(f"Processing word: '{word}' with tag: '{tag}'")

                # Retrieve existing tag from Tag table
                try:
                    tag = Tag.objects.get(name=tag)
                except Tag.DoesNotExist:
                    print(f"Tag '{tag}' does not exist in the Tag table.")
                    return JsonResponse({'status': 'error', 'message': f"Tag '{tag}' not found"}, status=400)

                # Save each word-tag pair to POSTag table
                postag = POSTag.objects.create(word=word, sentence=sentence, tag=tag)
                print(f"Saved POSTag entry: {postag}")

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def index(request):
    return render(request, 'Pos_app/index.html')
