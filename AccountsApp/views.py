from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from .forms import LoginForm, RegisterForm

import logging


logger = logging.getLogger(__name__)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('MelodyQuizApp:quiz_game_view')
            else:
                form.add_error('password', 'Invalid login credentials')

                logger.warning(f'Failed logging attempt for user: {username}')
    else:
        form = LoginForm()

    return render(request, 'AccountsApp/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            # Set the user instance for the password validation
            form.user = user

            user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, user)

            logger.info(f'User registered: {user.username}')

            return redirect('MelodyQuizApp:quiz_game_view')
    else:
        form = RegisterForm()

    return render(request, 'AccountsApp/registration.html', {'form': form})

