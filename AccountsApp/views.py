from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, authenticate


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('MelodyQuizApp:homepage')
            else:
                form.add_error('password', 'Invalid login credentials')
    else:
        form = LoginForm()

    return render(request, 'AccountsApp/login.html', {'form': form})


def register_view(request):
    return render(request, 'AccountsApp/registration.html') 