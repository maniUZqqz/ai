
# import speech_recognition as sr
#
# # ایجاد یک نمونه از کلاس Recognizer
# recognizer = sr.Recognizer()
#
# # استفاده از میکروفون برای ضبط صدا
# with sr.Microphone() as source:
#     print("لطفاً صحبت کنید...")
#     try:
#         # ضبط صدا
#         audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
#         print("صدا ضبط شد، در حال تبدیل به متن...")
#
#         # تبدیل صدا به متن
#         text = recognizer.  recognize_google(audio, language="en-US")  # تغییر زبان در صورت نیاز
#         print("متن شناسایی‌شده:")
#         print(text)
#     except sr.WaitTimeoutError:
#         print("زمان انتظار تمام شد، لطفاً دوباره امتحان کنید.")
#     except sr.UnknownValueError:
#         print("متوجه صحبت شما نشدم، لطفاً واضح‌تر صحبت کنید.")
#     except sr.RequestError as e:
#         print(f"خطا در ارتباط با سرویس تشخیص صدا: {e}")


QQZ = "pip install speech_recognition"

UZ = """

import speech_recognition as sr

# لیست زبان‌های پشتیبانی‌شده
languages = {
    "1": ("en-US", "English"),
    "2": ("fa-IR", "Farsi"),
    "3": ("ar-SA", "Arabic"),
    "4": ("fr-FR", "French"),
    "5": ("de-DE", "German"),
    "6": ("es-ES", "Spanish"),
    "7": ("it-IT", "Italian"),
    "8": ("zh-CN", "Chinese (Simplified)"),
    "9": ("ja-JP", "Japanese"),
    "10": ("ko-KR", "Korean"),
}

# نمایش لیست زبان‌ها
print("لطفاً زبان مورد نظر خود را انتخاب کنید:")
for key, (code, name) in languages.items():
    print(f"{key}: {name} ({code})")

# دریافت انتخاب کاربر
choice = input("شماره زبان را وارد کنید: ")

# بررسی انتخاب معتبر
if choice not in languages:
    print("انتخاب نامعتبر است. برنامه متوقف شد.")
else:
    language_code, language_name = languages[choice]
    print(f"شما زبان {language_name} ({language_code}) را انتخاب کردید.")

    # استفاده از میکروفون برای ضبط صدا
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"لطفاً به زبان {language_name} صحبت کنید...")
        try:
            # ضبط صدا
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("صدا ضبط شد، در حال تبدیل به متن...")

            # تبدیل صدا به متن
            text = recognizer.recognize_google(audio, language=language_code)
            print("متن شناسایی‌شده:")
            print(text)
        except sr.WaitTimeoutError:
            print("زمان انتظار تمام شد، لطفاً دوباره امتحان کنید.")
        except sr.UnknownValueError:
            print("متوجه صحبت شما نشدم، لطفاً واضح‌تر صحبت کنید.")
        except sr.RequestError as e:
            print(f"خطا در ارتباط با سرویس تشخیص صدا: {e}")


"""