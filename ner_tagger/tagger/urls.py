from django.urls import path
from tagger import views

urlpatterns = [
    path("", views.index, name='index'),
]