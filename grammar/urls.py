from django.urls import path
from . import views

urlpatterns = [
    path('', views.grammar, name='grammar'),
]

