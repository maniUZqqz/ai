from django.db import models

class Conversation(models.Model):
    user_question = models.TextField()  # سوال کاربر
    assistant_answer = models.TextField()  # پاسخ هوش مصنوعی
    timestamp = models.DateTimeField(auto_now_add=True)  # زمان ایجاد
    context_url = models.URLField(null=True, blank=True)  # ذخیره لینک محتوا
    title = models.CharField(max_length=255, null=True, blank=True)  # عنوان یا خلاصه چت
    is_active = models.BooleanField(default=False)  # آیا این چت فعال است؟

    def __str__(self):
        return self.title or "Untitled Chat"




# from django.db import models
#
#
# class Conversation(models.Model):
#     user_question = models.TextField()  # سوال کاربر
#     assistant_answer = models.TextField()  # پاسخ هوش مصنوعی
#     timestamp = models.DateTimeField(auto_now_add=True)  # زمان ایجاد
#     context_url = models.URLField(null=True, blank=True)  # ذخیره لینک محتوا
#
#     def __str__(self):
#         return f"Q: {self.user_question[:30]}... | A: {self.assistant_answer[:30]}..."



# class Message(models.Model):
#     ROLE_CHOICES = [
#         ('user', 'User'),
#         ('assistant', 'Assistant'),
#     ]
#
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.role}: {self.content[:50]}'
#
#
# class Conversation(models.Model):
#     user_question = models.TextField()  # سوال کاربر
#     assistant_answer = models.TextField()  # پاسخ هوش مصنوعی
#     timestamp = models.DateTimeField(auto_now_add=True)  # زمان ایجاد
#
#     def __str__(self):
#         return f"Q: {self.user_question[:30]}... | A: {self.assistant_answer[:30]}..."


