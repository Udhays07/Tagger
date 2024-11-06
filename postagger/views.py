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

        try:
            sentence_instance = Sentence.objects.get(id=sentence_id)

        except Sentence.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Sentence not found'}, status=400)

        for item in taggedWords:
            word, separator, tag = item.partition(':')
            if separator:
                try:
                    tag_instance = Tag.objects.get(name=tag.strip()) ## get with id 

                except Tag.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': f"Tag '{tag}' not found"}, status=400)

                POSTag.objects.create(word=word.strip(), sentence=sentence_instance, tag=tag_instance)

        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)

def index(request):
    return render(request, 'Pos_app/index.html')
