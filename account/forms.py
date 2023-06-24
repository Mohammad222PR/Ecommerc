from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserSingupForm(forms.Form):
    avatar = forms.ImageField(required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="Enter Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confrim Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username = username).exists()
        if user:
            raise ValidationError('Youre username has exist!')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email = email).exists()
        if user:
            raise ValidationError('Youre email has exist!')
        return email
    
    def clean(self):
        cd = super().clean()
        pass_1 = cd.get('password1')
        pass_2 = cd.get('password2')
        if pass_1 and pass_2 and pass_1 != pass_2:
            raise ValidationError('youre password is not mach!')
        
class UserLoginForm(forms.Form):
     email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
     password = forms.CharField(label="Enter Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))


class UserUpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',]
        

    

    