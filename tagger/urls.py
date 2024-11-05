# from django.urls import path
# from .views import index
# from . import views

# urlpatterns = [
#     path('', index, name='index'),  # Home page
#     path('save_ner/', views.save_ner_entry, name='save_ner_entry'),
#     path('fetch-existing-tags/', views.fetch_existing_tags, name='fetch_existing_tags'),
#     # path('save-sentences/', views.save_sentences, name='save_sentences'),
# ]

from django.urls import path
from . import views
from .views import update_tag, delete_tag, fetch_tag_table

urlpatterns = [
    path('', views.index, name='index'),
    path('save-sentences/', views.save_sentences, name='save_sentences'),
    path('save-tagged-words/', views.save_tagged_words, name='save_tagged_words'),
    path('fetch-tag-table/', views.fetch_tag_table, name='fetch_tag_table'),
    path('update-tag/', views.update_tag, name='update_tag'),
    path('delete-tag/<int:id>/', views.delete_tag, name='delete_tag'),
]