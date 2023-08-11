from django.shortcuts import redirect, render
from django.contrib.auth import logout


def homepage(request):
    return render(request, 'MelodyQuizApp/homepage.html')


def spotify_track_info(request):
    return render(request, 'spotify_auth_app/track_search.html')


def logout_view(request):
    logout(request)
    return redirect('MelodyQuizApp:homepage')