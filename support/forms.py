from django import forms
from .models import Ticket, TicketAnswer

class TicketandupdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title','body',]

    
    
