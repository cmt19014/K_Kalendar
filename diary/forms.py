from django import forms
from .models import DiaryEntry
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='必須。有効なメールアドレスを入力してください。')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['date', 'text']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'text': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
        }