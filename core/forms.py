from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['full_name', 'phone', 'service', 'date', 'time', 'message'] # فیلد time اضافه شد
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام و نام خانوادگی'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تماس'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.HiddenInput(), # چون با جاوااسکریپت مقدار می‌دهیم، مخفی باشد
            'time': forms.HiddenInput(), # چون با کلیک روی دکمه‌ها مقدار می‌دهیم، مخفی باشد
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }