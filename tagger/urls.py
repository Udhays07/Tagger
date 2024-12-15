from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('main1/', views.main1, name='main1'), 
    # path(''),
    # path('pos/', include('pos_tagger.urls')),
    path('ner-save-sentences/', views.ner_save_sentences, name='ner_save_sentences'),
    path('', views.tagger_index, name='tagger_index'),
    path('update-sentence-index/', views.update_sentence_index, name='update_sentence_index'),
    path('save-tagged-words/', views.save_tagged_words, name='save_tagged_words'),
    path('fetch-tag-table/', views.fetch_tag_table, name='fetch_tag_table'),
    # path('update-tag/', views.update_tag, name='update_tag'),
    # path('delete-tag/<int:id>/', views.delete_tag, name='delete_tag'),
]