from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    # path('', views.chat_room, name='chat_room'),
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]
