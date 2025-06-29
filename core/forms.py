from django import forms
from django.contrib.auth.models import User
from .models import Skill, ExchangeRequest, Message

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data["password"])  # Ensure the password is hashed
            user.save()
        return user

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['title', 'description', 'hourly_rate']

class ExchangeForm(forms.ModelForm):
    class Meta:
        model = ExchangeRequest
        fields = ['skill', 'hours_requested']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']

# core/forms.py





