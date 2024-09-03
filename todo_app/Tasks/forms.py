from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'complete', 'due_date', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Enter task title'}),
            'complete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }

class UserCreationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form', 'placeholder': 'Enter email address'}),
            'password1': forms.PasswordInput(attrs={'class': 'form', 'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form', 'placeholder': 'Confirm password'}),
        }

class ConfirmDeleteForm(forms.Form):
    confirm = forms.CheckboxInput(attrs={'class': 'form-check-input'})