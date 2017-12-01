from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()
class SignUpForm(UserCreationForm):
  	first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
  #	last_name  = forms.CharField(max_length=30, required=False, help_text='Optional')
  	email 	   = forms.EmailField(max_length=54, help_text='Required')
  	class Meta:
  		model = User
  		fields = ('first_name', 'email', 'username','password1', 'password2',
  				 )