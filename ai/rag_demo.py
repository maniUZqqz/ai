from openai import OpenAI
import requests
from bs4 import BeautifulSoup  # برای استخراج بهتر محتوا

API_KEY = 'tpsg-eG5ezeD7M8W2pQ3EfA3YqQ6gjYIaFfp'
BaseUrl = 'https://api.metisai.ir/openai/v1'

client = OpenAI(
    base_url=BaseUrl,
    api_key=API_KEY,
)

def urlRjinaAI(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # استخراج فقط متن مهم از صفحه
        return soup.get_text(separator="\n").strip()
    else:
        return "Error: Unable to fetch content"

# دریافت لینک و استخراج محتوا
content_url = input('Enter content URL: ')
content = urlRjinaAI(content_url)

if not content or "Error" in content:
    print("Error fetching content. Please check the URL.")
    exit()

system_prompt = f"""
You are a highly intelligent and helpful assistant.
Your purpose is to respond to user queries **only based on the content provided in the context**, shared in Markdown format.

- If the query cannot be answered using the context, respond with: "Answer not found".
- Do not provide answers or opinions beyond the context.
- Always keep your response concise and relevant to the query.

Website link: {content_url}

<context>
{content[:3000]}  # محدود کردن محتوا به تعداد کاراکترهای مجاز مدل
</context>
"""

conversation_history = [
    {"role": "system", "content": system_prompt}
]

while True:
    user_input = input("Enter your question (type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        print("Session ended.")
        break

    conversation_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history
    )

    # افزودن پاسخ مدل به تاریخچه
    assistant_reply = response.choices[0].message.content.strip()
    conversation_history.append({"role": "assistant", "content": assistant_reply})

    print("Answer:", assistant_reply)



