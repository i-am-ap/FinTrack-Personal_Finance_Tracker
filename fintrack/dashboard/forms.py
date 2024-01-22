from django import forms
from .models import CustomUser

class SignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password']
    widgets = {
        'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
    }
    

class ReportForm(forms.Form):
    month = forms.IntegerField(label='Month', min_value=1, max_value=12)
    year = forms.IntegerField(label='Year', min_value=1900)