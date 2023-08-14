from django.shortcuts import render, redirect



def login(request):
    return render(request, 'AccountsApp/login.html')


def register(request):
    return render(request, 'AccountsApp/registration.html') 