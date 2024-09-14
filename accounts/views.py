from django.shortcuts import render
import uuid
import sys
from django.shortcuts import render
from django.core.mail import send_mail
from accounts.models import Token
from django.contrib.auth import login as auth_login, logout as auth_logout
import uuid
import sys
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.mail import send_mail
from django.shortcuts import redirect, render


def send_login_email(request):
    """выслать ссылку на логин по почте"""
    email = request.POST["email"]
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print("saving uid", uid, "for email", email, file=sys.stderr)
    url = request.build_absolute_uri(f"/accounts/login?uid={uid}")
    send_mail(
        "Your login link for Superlists",
        f"Use this link to log in:\n\n{url}",
        "noreply@superlists",
        [email],
    )

    return render(request, "login_email_sent.html")


def login(request):
    '''регистрация в системе'''

    print('login view', file=sys.stderr)
    uid = request.GET.get('uid')
    user = authenticate(uid=uid)
    if user is not None:
        auth_login(request, user)
    return redirect('/')


def logout(request):
    '''выход из системы'''
    auth_logout(request)
    return redirect('/')
