from django.urls import path
from . import views


urlpatterns = [
    path("", views.rag, name="Rag"),
    path('add_url/', views.add_url, name='add_url'),
    path('chat_with_bot/', views.chat_with_bot, name='chat_with_bot'),
    # path("upload_file/", views.upload_file, name="upload_file"),
    # path("crawl_website/", views.crawl_website, name="crawl_website"),
    # path("handle_chat/", views.handle_chat, name="handle_chat"),
    # path("load_chats/", views.load_chats, name="load_chats"),
]
