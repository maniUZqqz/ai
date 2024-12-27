import whisper
from openai import OpenAI
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile

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

# تابع ضبط صدا
def record_audio(duration=10, sample_rate=16000):
    print(f"Recording for {duration} seconds...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()  # انتظار برای اتمام ضبط
    print("Recording complete.")
    return audio_data, sample_rate

# تبدیل صدای ضبط‌شده به متن
def transcribe_audio(audio_data, sample_rate):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_wav:
        write(temp_wav.name, sample_rate, audio_data)  # ذخیره صدای ضبط‌شده در فایل موقت
        result = whisper_model.transcribe(temp_wav.name)  # تبدیل صدا به متن
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

# حلقه برای ضبط صدا و پردازش
while True:
    print("\nPress Enter to start recording, or type 'exit' to quit.")
    command = input(">>> ")
    if command.lower() == 'exit':
        print("Exiting...")
        break

    # ضبط صدا
    audio_data, sample_rate = record_audio(duration=10)  # ضبط صدا به مدت 10 ثانیه
    user_input = transcribe_audio(audio_data, sample_rate)  # تبدیل صدا به متن
    print("\nTranscribed Text:", user_input)

    # استخراج اطلاعات کلیدی
    key_info = extract_key_information(user_input)
    print("Extracted Information:", key_info)
