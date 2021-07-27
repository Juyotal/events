from .models import Event, Discount
from django import forms


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['guests', 'booked']


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = '__all__'
