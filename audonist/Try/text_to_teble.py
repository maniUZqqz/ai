from openai import OpenAI

# تنظیم اطلاعات API
API_KEY = 'tpsg-eG5ezeD7M8W2pQ3EfA3YqQ6gjYIaFfp'
BaseUrl = 'https://api.metisai.ir/openai/v1'

# اتصال به کلاینت متیس
client = OpenAI(
    base_url=BaseUrl,
    api_key=API_KEY,
)

# تعریف تابع برای استخراج اطلاعات
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

# حلقه دریافت ورودی کاربر
while True:
    user_input = input("Enter your text (type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        print("Exiting...")
        break

    key_info = extract_key_information(user_input)
    print("Extracted Information:", key_info)
