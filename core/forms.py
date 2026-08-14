from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['full_name', 'phone', 'service', 'message'] # date و time حذف شدند
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'مثال: علی محمدی'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': '۰۹۱۲۳۴۵۶۷۸۹'}),
            'service': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'توضیحات لازم برای دکتر...'}),
        }