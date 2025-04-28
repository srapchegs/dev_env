from django.shortcuts import render
from users.forms import UserLoginForm,UserRegistrationForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages  # добавляем импорт


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, f'Вы успешно вошли как {user.username}!')
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()
    context = {
        'title': "Авторизация",
        "form": form
    }
    return render(request, 'users/login.html', context)

def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(request, f'Регистрация прошла успешно! Добро пожаловать, {user.username}!')
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()
    context = {
        'title': "Регистрация",
        "form": form
    }
    return render(request, 'users/registration.html', context)

def profile(request):
    context = {
        'title': "Личный кабинет"
    }   
    return render(request,'users/purchase.html', context)

def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))