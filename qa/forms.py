from django import forms
from django.contrib.auth.models import User

from .models import *

class UserdetailsForm(forms.ModelForm):

    class Meta:
        model = Userdetails
        fields = ['USN', 'name', 'branch', 'semester']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


        
class QuestionForm(forms.ModelForm):

	class Meta:
		model=Questions
		fields=['questionfield']



class AnswerForm(forms.ModelForm):
	class Meta:
		model=Answers
		fields=['answer']

class BlogForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields=['title','content']
class TagForm(forms.ModelForm):
    class Meta:
        model=Tags
        fields=['tag_name']
