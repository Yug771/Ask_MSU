# qa_app/forms.py

from django import forms
from .models import Question, User
from django.contrib.auth import get_user_model

User = get_user_model()

class QuestionForm(forms.Form):
    question_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2.5, 'cols': 70.5}),
        label='Your Question',
        help_text="<span style='color:green'>Enter your question here.</span>"
    )

from django.contrib.auth.forms import UserCreationForm
from .models import User  # Import your custom User model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
