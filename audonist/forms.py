from django import forms


class audonistForm(forms.Form):
    text = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={
            'placeholder': 'متن خود را وارد کنید...',  # مثال: متن پیش‌فرض
            'rows': 5,  # تعداد سطرها
            'cols': 40,  # تعداد ستون‌ها (اختیاری)
        })
    )

