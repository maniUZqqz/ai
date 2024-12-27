from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
from openai import OpenAI

API_KEY = 'tpsg-eG5ezeD7M8W2pQ3EfA3YqQ6gjYIaFfp'
BaseUrl = 'https://api.metisai.ir/openai/v1'

client = OpenAI(
    base_url=BaseUrl,
    api_key=API_KEY,
)


def index(request):
    return render(request,'ai/chat.html')






# @login_required
# def chat_room(request):
#     if request.method == 'POST':
#         content = request.POST.get('content')
#         receiver_id = request.POST.get('receiver_id')
#         if content and receiver_id:
#             receiver = User.objects.get(id=receiver_id)
#             Message.objects.create(sender=request.user, receiver=receiver, content=content)
#
#     messages = Message.objects.filter(receiver=request.user) | Message.objects.filter(sender=request.user)
#     return render(request, 'chat/chat_room.html', {'messages': messages})
