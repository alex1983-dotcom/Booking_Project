from django import forms
from .models.booking_models import Feedback, Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__' 


class FeedbackAdminForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры.")
        if len(phone_number) < 10 or len(phone_number) > 15:
            raise forms.ValidationError("Введите номер телефона длиной от 10 до 15 цифр.")
        return phone_number
