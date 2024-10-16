from django.urls import path
from .views import index
from . import views

urlpatterns = [
    path('', index, name='index'),  # Home page
    path('save_ner/', views.save_ner_entry, name='save_ner_entry'),
    path('fetch-existing-tags/', views.fetch_existing_tags, name='fetch_existing_tags'),
]
