from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('save-sentence/', views.save_sentence, name='save_sentence'),
    path('save-tags/', views.save_pos_tags, name='save_pos_tags'),
]

