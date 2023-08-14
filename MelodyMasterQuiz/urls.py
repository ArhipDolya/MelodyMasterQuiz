from django.contrib import admin
from django.urls import path, include

from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/quiz/')),
    path('', include('spotify_auth_app.urls')),
    path('quiz/', include('MelodyQuizApp.urls')),
    path('accounts/', include('AccountsApp.urls')),
]
