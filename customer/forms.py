from django import forms
from django.contrib.auth.models import User
from .models import ResetPassword



class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50, label='', widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, label='', widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Last Name'}))
    username = forms.CharField(max_length=50, label='', widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Username'}))
    email = forms.EmailField(max_length=50, label='', widget=forms.EmailInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Email'}))
    password = forms.CharField(max_length=50, label='', widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Password'}))
    password_again = forms.CharField(max_length=50, label='', widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Password Again'}))



class PasswordResetForm(forms.Form):
    token = forms.CharField(widget=forms.HiddenInput())
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password_again = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}))


    def clean(self):
        cleaned_data = super().clean()
        token = cleaned_data['token']
        username = cleaned_data['username']
        password = cleaned_data['password']
        password_again = cleaned_data['password_again']
        rp = ResetPassword.objects.filter(token=token).first()
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError('User not found')
        if not rp or rp.user != user:
            raise forms.ValidationError('Process failed')
        
        if password and password_again and password != password_again:
            raise forms.ValidationError('Passwords do not match')
        
        return cleaned_data
    

    def save(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data['username']
        password = cleaned_data['password']
        token = cleaned_data['token']
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        rp = ResetPassword.objects.get(token=token)
        rp.used = True
        rp.save()
        return user
