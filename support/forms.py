from django import forms
from .models import Ticket, TicketAnswer

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title','body','images',]

    images = forms.ImageField(required=False)
    
class TicketAnswerForm(forms.ModelForm):
    class Meta:
        model = TicketAnswer
        fields = ['ticket', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ticket'].widget = forms.HiddenInput()
        self.fields['body'].widget = forms.Textarea()