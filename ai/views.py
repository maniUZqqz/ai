from django.shortcuts import render, redirect
from django.http import JsonResponse
from openai import OpenAI
from .models import Conversation
import requests
from bs4 import BeautifulSoup
from django.utils.text import Truncator

API_KEY = 'tpsg-eG5ezeD7M8W2pQ3EfA3YqQ6gjYIaFfp'
BaseUrl = 'https://api.metisai.ir/openai/v1'

client = OpenAI(
    base_url=BaseUrl,
    api_key=API_KEY,
)

# تابع برای استخراج محتوا از URL
def extract_content_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator="\n").strip()
    except Exception as e:
        return None

def home(request):
    conversations = Conversation.objects.all().order_by('-timestamp')
    active_chat = conversations.filter(is_active=True).first()

    if request.method == 'POST':
        user_input = request.POST.get('message', '').strip()
        url_input = request.POST.get('url', '').strip()

        if not user_input and not url_input:
            return JsonResponse({"error": "Input is required"}, status=400)

        try:
            if user_input:
                # درخواست به OpenAI با پیام کاربر
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": user_input}]
                )
                answer = response.choices[0].message.content
                title = Truncator(answer).words(5)

                conversation = Conversation.objects.create(
                    user_question=user_input,
                    assistant_answer=answer,
                    title=title,
                    is_active=True
                )
                return JsonResponse({"answer": answer, "title": title})

            if url_input:
                content = extract_content_from_url(url_input)
                if not content:
                    return JsonResponse({"error": "Invalid URL content"}, status=400)

                # درخواست به OpenAI با استفاده از محتوا از URL
                system_prompt = f"""
                You are a highly intelligent and helpful assistant.
                Your purpose is to respond to user queries **only based on the content provided in the context**, shared in Markdown format.

                - If the query cannot be answered using the context, respond with: "Answer not found".
                - Do not provide answers or opinions beyond the context.
                - Always keep your response concise and relevant to the query.

                Website link: {url_input}

                <context>
                {content[:3000]}  # محدود کردن محتوا به تعداد کاراکترهای مجاز مدل
                </context>
                """
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": system_prompt}]
                )
                answer = response.choices[0].message.content
                title = Truncator(answer).words(5)

                conversation = Conversation.objects.create(
                    user_question=f"Content URL: {url_input}",
                    assistant_answer=answer,
                    context_url=url_input,
                    title=title,
                    is_active=True
                )
                return JsonResponse({"answer": answer, "title": title})

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return render(request, 'ai/home.html', {'conversations': conversations, 'active_chat': active_chat})


def header(request):
    return render(
        request,
        'base/header.html',
        {}
    )


def footer(request):
    return render(
        request,
        'base/footer.html',
        {}
    )






# def urlRjinaAI(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, "html.parser")
#         return soup.get_text(separator="\n").strip()
#     else:
#         return "Error: Unable to fetch content"
#
#
# def home(request):
#     if request.method == 'POST':
#         user_input = request.POST.get('message')
#         url_input = request.POST.get('url')
#
#         if not user_input and not url_input:
#             return JsonResponse({"error": "Message or URL is required."}, status=400)
#
#         if url_input:  # اگر URL وارد شده بود، محتوا استخراج شود
#             content = urlRjinaAI(url_input)
#             if "Error" in content:
#                 return JsonResponse({"error": content}, status=400)
#
#             system_prompt = f"""
#             You are a highly intelligent and helpful assistant.
#             Your purpose is to respond to user queries **only based on the content provided in the context**, shared in Markdown format.
#             Website link: {url_input}
#
#             <context>
#             {content[:3000]}
#             </context>
#             """
#         else:
#             system_prompt = "You are a general assistant."
#
#         # ارسال به مدل
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}]
#         )
#
#         answer = response.choices[0].message.content
#
#         # ذخیره سوال و جواب در Conversation
#         conversation = Conversation.objects.create(
#             user_question=user_input,
#             assistant_answer=answer,
#             context_url=url_input  # ذخیره URL چنانچه وجود داشته باشد
#         )
#
#         return JsonResponse({"answer": answer})
#
#     return render(request, 'ai/home.html')

m = "========"

# def home(request):
#     if request.method == 'POST':
#         user_input = request.POST.get('message')
#         if not user_input:
#             return JsonResponse({"error": "Message is required."}, status=400)
#
#         # ارسال به مدل
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[{"role": "user", "content": user_input}],
#         )
#
#         # استخراج پاسخ مدل
#         answer = response.choices[0].message.content
#
#         # ذخیره سوال و جواب در Conversation
#         conversation = Conversation.objects.create(
#             user_question=user_input,
#             assistant_answer=answer
#         )
#
#         return JsonResponse({"answer": answer})
#
#     return render(request, 'ai/home.html')