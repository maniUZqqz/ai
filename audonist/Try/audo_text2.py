import whisper
from openai import OpenAI
import os

file_path = "/audonist/Try/QQZ.mp3"
if not os.path.exists(file_path):
    print("File not found. Please check the path.")
else:
    print("File exists!")




# تنظیم اطلاعات API
API_KEY = 'tpsg-eG5ezeD7M8W2pQ3EfA3YqQ6gjYIaFfp'
BaseUrl = 'https://api.metisai.ir/openai/v1'

# اتصال به کلاینت متیس
client = OpenAI(
    base_url=BaseUrl,
    api_key=API_KEY,
)

# بارگذاری مدل Whisper
whisper_model = whisper.load_model("base")

# تبدیل فایل صوتی به متن
def transcribe_audio_from_file(file_path):
    print(f"Processing file: {file_path}")
    result = whisper_model.transcribe(file_path)  # تبدیل صدا به متن
    return result["text"]

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

# حلقه برای پردازش فایل صوتی
while True:
    print("\nEnter the path to your audio file, or type 'exit' to quit.")
    command = input(">>> ")
    if command.lower() == 'exit':
        print("Exiting...")
        break

    try:
        # تبدیل صدا به متن
        user_input = transcribe_audio_from_file(command)
        print("\nTranscribed Text:", user_input)

        # استخراج اطلاعات کلیدی
        key_info = extract_key_information(user_input)
        print("Extracted Information:", key_info)

    except FileNotFoundError:
        print("File not found. Please enter a valid path.")
    except Exception as e:
        print("An error occurred:", e)


p = "E:\tamrin\AI\QQZai\Try\QQZ.mp3"