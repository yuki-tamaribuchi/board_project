from .models import Profile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username','password1','password2')
        

class RegistProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('handle','location','biograph')



class LoginForm(AuthenticationForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['password'].widget.attrs['class']='form-control'