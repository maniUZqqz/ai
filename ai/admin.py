from django.contrib import admin
from .models import Conversation


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('user_question', 'assistant_answer', 'timestamp')  # ستون‌های نمایش داده شده
    search_fields = ('user_question', 'assistant_answer')  # قابلیت جستجو
    list_filter = ('timestamp',)  # فیلتر بر اساس زمان



# @admin.register(Message)
# class MessageAdmin(admin.ModelAdmin):
#     list_display = ('role', 'content', 'timestamp')  # ستون‌های قابل نمایش
#     list_filter = ('role', 'timestamp')  # فیلترهای قابل استفاده
#     search_fields = ('content',)  # قابلیت جستجو در متن
#
