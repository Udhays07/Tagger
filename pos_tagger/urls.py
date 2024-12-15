from django.urls import path, include
from . import views

urlpatterns = [
    path('pos_tagger/', views.index, name='pos_index'),
    path('pos-save-sentences/', views.pos_save_sentences, name='pos_save_sentences'),
    path('main/', views.main, name='main'), 
    path('pos_tagger/save-tagged-words/', views.save_tagged_words, name='save_tagged_words'),
    path('', views.pos_tagger_index, name='pos_tagger_index'), 
    path('pos_tagger/update-sentence-index/', views.update_sentence_index, name='update_sentence_index'),
]