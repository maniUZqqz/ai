from django.shortcuts import render, redirect
from django.http import JsonResponse
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
from django.utils.text import Truncator
from .forms import audonistForm


API_KEY = 'tpsg-eG5ezeD7M8W2pQ3EfA3YqQ6gjYIaFfp'
BaseUrl = 'https://api.metisai.ir/openai/v1'

client = OpenAI(
    base_url=BaseUrl,
    api_key=API_KEY,
)


def extract_key_information(user_input):
    messages = [
        {"role": "system", "content": "You are an assistant that extracts key information from a given text and outputs it as a dictionary."},
        {"role": "user", "content": f"Extract the key information from the following text:\n\n{user_input}"}
    ]

    # ارسال درخواست به متیس
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # مدل استفاده‌شده
        messages=messages
    )

    # استخراج پاسخ مدل
    response_dict = response.to_dict()

    # بازگشت پاسخ به‌عنوان دیکشنری
    try:
        structured_output = eval(response_dict['choices'][0]['message']['content'])
        return structured_output
    except Exception as e:
        print("Error parsing structured output:", e)
        return response_dict['choices'][0]['message']['content']

def audo(request):
    user_input = None  # مقدار پیش‌فرض برای ورودی کاربر
    key_info = None    # مقدار پیش‌فرض برای خروجی پردازش‌شده

    if request.method == "POST":
        form = audonistForm(request.POST)
        if form.is_valid():
            # داده‌های فرم معتبر هستند
            user_input = form.cleaned_data['text']
            key_info = extract_key_information(user_input)
    else:
        form = audonistForm()

    return render(
        request,
        'audo/audo.html',
        {
            'form': form,
            'user_input': user_input,
            'key_info': key_info,
        }
    )
