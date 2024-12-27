from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from .models import URLContent, Chat, Message
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI

API_KEY = 'tpsg-eG5ezeD7M8W2pQ3EfA3YqQ6gjYIaFfp'
BaseUrl = 'https://api.metisai.ir/openai/v1'

client = OpenAI(
    base_url=BaseUrl,
    api_key=API_KEY,
)


def send_message(request):
    if request.method == 'POST':
        chat_id = request.POST.get('chat_id')
        content = request.POST.get('content')
        chat = Chat.objects.get(id=chat_id)
        message = Message.objects.create(chat=chat, content=content, role='user')
        return JsonResponse({'status': 'success', 'message': 'Message sent successfully'})

def send_link(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        URLContent.objects.create(url=url)
        return JsonResponse({'status': 'success', 'message': 'Link sent successfully'})





# رندر صفحه اصلی
def rag(request):
    if request.method == 'POST':
        user_input = request.POST.get('message')
        if not user_input:
            return JsonResponse({"error": "Message is required."}, status=400)

        # ارسال به مدل
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_input}],
        )

        # استخراج پاسخ مدل
        answer = response.choices[0].message.content

        # ذخیره سوال و جواب در Conversation
        conversation = Conversation.objects.create(
            user_question=user_input,
            assistant_answer=answer
        )

        return JsonResponse({"answer": answer})
    return render(request, 'rag/rag.html')















def extract_content_from_url(url):
    """استخراج محتوای متنی از URL"""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator="\n").strip()
    return None


@csrf_exempt
def add_url(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body.decode("utf-8"))
        url = data.get("url")

        if not url:
            return JsonResponse({"error": "URL is required"}, status=400)

        content = extract_content_from_url(url)
        if not content:
            return JsonResponse({"error": "Failed to fetch content"}, status=400)

        # ذخیره محتوای لینک در پایگاه داده
        url_entry = URLContent.objects.create(url=url, content=content)
        return JsonResponse({"message": "URL content saved", "id": url_entry.id})
    return JsonResponse({"error": "Invalid request method"}, status=405)











@csrf_exempt
def send_message(request):
    """ارسال پیام به چت فعال"""
    if request.method == 'POST':
        import json
        data = json.loads(request.body.decode("utf-8"))
        chat_id = data.get("chat_id")
        content = data.get("content")

        if not chat_id or not content:
            return JsonResponse({"error": "Chat ID and content are required"}, status=400)

        # دریافت چت
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return JsonResponse({"error": "Chat not found"}, status=404)

        # ذخیره پیام کاربر
        Message.objects.create(chat=chat, role="user", content=content)

        # ارسال درخواست به OpenAI
        url_content = URLContent.objects.first()
        if not url_content:
            return JsonResponse({"error": "No context available"}, status=400)

        # تاریخچه مکالمه
        system_prompt = f"""
        You are a helpful assistant. 
        Respond to questions based **only on the context provided below**:

        <context>
        {url_content.content[:3000]}
        </context>
        """

        conversation_history = [{"role": "system", "content": system_prompt}]
        for message in chat.messages.all():
            conversation_history.append({"role": message.role, "content": message.content})

        # اضافه کردن پیام کاربر
        conversation_history.append({"role": "user", "content": content})

        # پاسخ OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history
        )
        assistant_reply = response.choices[0].message.content.strip()

        # ذخیره پاسخ
        Message.objects.create(chat=chat, role="assistant", content=assistant_reply)

        return JsonResponse({"answer": assistant_reply})
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def add_url(request):
    """اضافه کردن لینک"""
    if request.method == "POST":
        import json
        data = json.loads(request.body.decode("utf-8"))
        url = data.get("url")

        if not url:
            return JsonResponse({"error": "URL is required"}, status=400)

        content = extract_content_from_url(url)
        if not content:
            return JsonResponse({"error": "Failed to fetch content"}, status=400)

        # ذخیره محتوای لینک
        url_entry = URLContent.objects.create(url=url, content=content)
        return JsonResponse({"message": "URL content saved", "id": url_entry.id})
    return JsonResponse({"error": "Invalid request method"}, status=405)


def extract_content_from_url(url):
    """استخراج محتوا از لینک"""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator="\n").strip()
    return None








@csrf_exempt
def chat_with_bot(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body.decode("utf-8"))
        chat_id = data.get("chat_id")
        question = data.get("question")

        if not chat_id or not question:
            return JsonResponse({"error": "Chat ID and question are required"}, status=400)

        # بررسی اینکه آیا چت وجود دارد
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return JsonResponse({"error": "Chat not found"}, status=404)

        # استفاده از محتوای لینک برای پاسخ‌دهی
        url_content = URLContent.objects.first()  # اولین URL ذخیره شده
        if not url_content:
            return JsonResponse({"error": "No context available"}, status=400)

        # آماده‌سازی تاریخچه مکالمه
        system_prompt = f"""
        You are a helpful assistant.
        Respond to questions based **only on the context provided below**:

        <context>
        {url_content.content[:3000]}
        </context>
        """

        conversation_history = [{"role": "system", "content": system_prompt}]
        for message in chat.messages.all():
            conversation_history.append({"role": message.role, "content": message.content})

        # اضافه کردن پیام کاربر
        conversation_history.append({"role": "user", "content": question})

        # ارسال پیام به OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history
        )

        assistant_reply = response.choices[0].message.content.strip()

        # ذخیره پیام در پایگاه داده
        Message.objects.create(chat=chat, role="user", content=question)
        Message.objects.create(chat=chat, role="assistant", content=assistant_reply)

        return JsonResponse({"answer": assistant_reply})
    return JsonResponse({"error": "Invalid request method"}, status=405)





# from django.shortcuts import render
# import requests
# from bs4 import BeautifulSoup
# from django.http import JsonResponse
# from .models import URLContent
# from django.views.decorators.csrf import csrf_exempt
# from .models import Chat, Message
# from openai import OpenAI
# from django.http import JsonResponse
# from .models import URLContent, Chat, Message
#
#
# API_KEY = 'tpsg-eG5ezeD7M8W2pQ3EfA3YqQ6gjYIaFfp'
# BaseUrl = 'https://api.metisai.ir/openai/v1'
#
# client = OpenAI(
#     base_url=BaseUrl,
#     api_key=API_KEY,
# )
#
#
#
#






# # Function to chunk text
# def chunk_text(text, chunk_size=500):
#     words = text.split()
#     for i in range(0, len(words), chunk_size):
#         yield " ".join(words[i:i + chunk_size])
#
# # Upload and process files
# @csrf_exempt
# def upload_file(request):
#     if request.method == "POST" and request.FILES.get("file"):
#         uploaded_file = request.FILES["file"]
#         file_instance = FileUpload.objects.create(name=uploaded_file.name, file=uploaded_file)
#
#         # Process the file content
#         fs = FileSystemStorage()
#         file_path = fs.path(file_instance.file.name)
#         try:
#             with open(file_path, "r", encoding="utf-8") as f:
#                 content = f.read()
#                 markdown_chunks = list(chunk_text(content))
#                 file_instance.processed_content = "\n\n".join(markdown_chunks)
#                 file_instance.save()
#             return JsonResponse({"status": "success", "chunks": markdown_chunks})
#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)})
#     return JsonResponse({"status": "error", "message": "No file uploaded"})
#
# # Crawl and chunk website
# @csrf_exempt
# def crawl_website(request):
#     if request.method == "POST":
#         url = request.POST.get("url")
#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 soup = BeautifulSoup(response.content, "html.parser")
#                 text = soup.get_text(separator="\n")
#                 chunks = list(chunk_text(text))
#
#                 # Save content and chunks to the database
#                 WebsiteContent.objects.create(
#                     url=url, title=soup.title.string if soup.title else "No Title", content_chunks=chunks
#                 )
#                 return JsonResponse({"status": "success", "chunks": chunks})
#             return JsonResponse({"status": "error", "message": "Failed to fetch URL"})
#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)})
#     return JsonResponse({"status": "error", "message": "Invalid request method"})
#
# # Handle chat messages
# @csrf_exempt
# def handle_chat(request):
#     if request.method == "POST":
#         session_id = request.POST.get("session_id")
#         user_message = request.POST.get("message")
#         if not session_id:
#             session = ChatSession.objects.create()
#             session_id = session.id
#         else:
#             session = ChatSession.objects.get(id=session_id)
#
#         # Save user message
#         ChatMessage.objects.create(session=session, role="user", message=user_message)
#
#         # Generate assistant response (dummy for now)
#         assistant_response = f"AI Response to: {user_message}"
#         ChatMessage.objects.create(session=session, role="assistant", message=assistant_response)
#
#         # Retrieve full chat history
#         chat_history = list(session.messages.values("role", "message", "timestamp"))
#         return JsonResponse({"status": "success", "session_id": session.id, "chat_history": chat_history})
#     return JsonResponse({"status": "error", "message": "Invalid request method"})
#
# # Load chat sessions
# def load_chats(request):
#     sessions = ChatSession.objects.all().values("id", "title", "created_at")
#     return JsonResponse({"sessions": list(sessions)})
