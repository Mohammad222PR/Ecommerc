from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title','body','images',]

    images = forms.ImageField(required=False)
    