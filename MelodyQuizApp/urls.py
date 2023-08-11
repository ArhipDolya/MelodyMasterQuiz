from django.urls import path

from . import views


app_name = 'MelodyQuizApp'

urlpatterns = [
    path('', views.homepage, name='homepage'),

]
