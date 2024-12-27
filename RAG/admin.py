from django.contrib import admin
from .models import URLContent, Chat, Message

@admin.register(URLContent)
class URLContentAdmin(admin.ModelAdmin):
    list_display = ("id", "url")
    search_fields = ("url",)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat", "role", "content", "created_at")
    list_filter = ("role", "created_at")
    search_fields = ("content",)



# from django.contrib import admin
# from .models import FileUpload, WebsiteContent, ChatSession, ChatMessage
#
# @admin.register(FileUpload)
# class FileUploadAdmin(admin.ModelAdmin):
#     list_display = ('name', 'uploaded_at', 'file')
#
# @admin.register(WebsiteContent)
# class WebsiteContentAdmin(admin.ModelAdmin):
#     list_display = ('url', 'title', 'crawled_at')
#
# @admin.register(ChatSession)
# class ChatSessionAdmin(admin.ModelAdmin):
#     list_display = ('title', 'created_at')
#
# @admin.register(ChatMessage)
# class ChatMessageAdmin(admin.ModelAdmin):
#     list_display = ('session', 'role', 'message', 'timestamp')
