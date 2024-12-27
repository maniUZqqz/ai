from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
from .models import Message

API_KEY = 'tpsg-eG5ezeD7M8W2pQ3EfA3YqQ6gjYIaFfp'
BaseUrl = 'https://api.metisai.ir/openai/v1'

# ذخیره تاریخچه مکالمات
conversation_history = []

# تعریف کلاینت
client = OpenAI(
    base_url=BaseUrl,
    api_key=API_KEY,
)

def grammar(request):
    if request.method == 'POST':
        user_input = request.POST.get('message')
        if not user_input:
            return JsonResponse({"error": "Message is required."}, status=400)

        # متن اصلاح گرامری
        grammar_request = f"Correct the grammar of the following text: \"{user_input}\""

        # ذخیره پیام کاربر در دیتابیس
        user_message = Message.objects.create(role='user', content=user_input)

        # افزودن پیام کاربر به تاریخچه
        conversation_history.append({"role": "user", "content": grammar_request})

        # ارسال به مدل
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
        )

        # استخراج پاسخ
        answer = response.choices[0].message.content

        # ذخیره پاسخ مدل در دیتابیس
        assistant_message = Message.objects.create(role='assistant', content=answer)

        # افزودن پاسخ مدل به تاریخچه
        conversation_history.append({"role": "assistant", "content": answer})

        return JsonResponse({"corrected_text": answer})

    return render(request, 'grammer/grammar.html')
