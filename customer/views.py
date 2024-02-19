from django.shortcuts import render, get_object_or_404
from .models import Customer, ResetPassword
from .forms import LoginForm, RegisterForm, PasswordResetForm
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['password_again']:
                user = User.objects.create_user(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                )
                customer = Customer.objects.create(user=user)
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'register.html', {'form': form, 'error': 'Passwords do not match'})
    form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # remember = request.POST.get('remember', False)
        user = authenticate(username=username, password=password)
        customer = Customer.objects.get(user=user)
        if user and customer:
            login(request, user)
            # if not remember:
            #     request.session.set_expiry(0)
            return redirect('home')
        return render(request, 'login.html', {'login': login, 'error': 'Invalid username or password',})
    return render(request, 'login.html', {'login': login})


def logout_view(request):
    logout(request)
    return redirect('login')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            ResetPassword.objects.filter(user=user).update(used=True)
            rp = ResetPassword.objects.create(user=user)
            url = request.build_absolute_uri(rp.get_absolute_url())
            message = f'Please renew your password from this link: {url}'
            subject = 'Renew your password'
            sender = settings.EMAIL_HOST_USER
            send_mail(subject, message, sender, [email])
            return redirect('reset-password-result', color='success', message='Mail sent successfully')
        else:
            return render(request, 'forgot_password.html', {'status': 'invalid_user'})
    
    return render(request, 'forgot_password.html')



def reset_password_view(request, token):
    rp = ResetPassword.objects.filter(token=token).first()
    if rp and rp.is_valid():
        if request.method == 'GET':
            form = PasswordResetForm(initial={'token': token})
            return render(request, 'reset-password.html', {'form': form})
        else:
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('reset-password-result', color='success', message='Password changed successfully')
            return render(request, 'reset-password.html', {'form': form})
    else:
        return redirect('reset-password-result', color='danger', message='The reset password link is invalid or expired')


def reset_password_result_view(request, color, message):
    return render(request, 'reset-password-result.html', {'color': color, 'message': message})