# from django.urls import path
# from .views import index
# from . import views

# urlpatterns = [
#     path('', index, name='index'),  # Home page
#     path('save_ner/', views.save_ner_entry, name='save_ner_entry'),
#     path('fetch-existing-tags/', views.fetch_existing_tags, name='fetch_existing_tags'),
#     # path('save-sentences/', views.save_sentences, name='save_sentences'),
# ]

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('main1/', views.main1, name='main1'), 
    # path(''),
    # path('pos/', include('pos_tagger.urls')),
    path('ner-save-sentences/', views.ner_save_sentences, name='ner_save_sentences'),
    path('', views.tagger_index, name='tagger_index'),
    path('save-tagged-words/', views.save_tagged_words, name='save_tagged_words'),
    path('update-sentence-index/', views.update_sentence_index, name='update_sentence_index'),
]