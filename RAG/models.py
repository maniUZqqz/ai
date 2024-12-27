from django.db import models

class URLContent(models.Model):
    url = models.URLField()
    content = models.TextField()  # محتوای متنی استخراج شده
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url

class Chat(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=50, choices=[("user", "User"), ("assistant", "Assistant")])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} ({self.chat.name}): {self.content[:30]}"


class Conversation(models.Model):
    user_question = models.TextField()  # سوال کاربر
    assistant_answer = models.TextField()  # پاسخ هوش مصنوعی
    timestamp = models.DateTimeField(auto_now_add=True)  # زمان ایجاد

    def __str__(self):
        return f"Q: {self.user_question[:30]}... | A: {self.assistant_answer[:30]}..."




# from django.db import models
#
# class Conversation(models.Model):
#     user_question = models.TextField()  # سوال کاربر
#     assistant_answer = models.TextField()  # پاسخ هوش مصنوعی
#     timestamp = models.DateTimeField(auto_now_add=True)  # زمان ذخیره
#
#     def __str__(self):
#         return f"Q: {self.user_question[:50]}... | A: {self.assistant_answer[:50]}..."
#
# class FileUpload(models.Model):
#     name = models.CharField(max_length=255)
#     file = models.FileField(upload_to="uploads/")
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     processed_content = models.TextField(blank=True)  # اطلاعات مارک‌داون شده
#
# class WebsiteContent(models.Model):
#     url = models.URLField()
#     title = models.CharField(max_length=255)
#     content_chunks = models.JSONField()  # ذخیره چانک‌ها به صورت JSON
#     crawled_at = models.DateTimeField(auto_now_add=True)
#
# class ChatSession(models.Model):
#     title = models.CharField(max_length=255, blank=True)  # ذخیره عنوان چت
#     created_at = models.DateTimeField(auto_now_add=True)
#
# class ChatMessage(models.Model):
#     session = models.ForeignKey(ChatSession, related_name="messages", on_delete=models.CASCADE)
#     role = models.CharField(max_length=50, choices=[('user', 'User'), ('assistant', 'Assistant')])
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
