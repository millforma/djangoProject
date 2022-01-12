from django.conf import settings
from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.conf.urls.static import static

from thousand_one_inventions.views import RegisterView, ProfileView

urlpatterns = [
    path("", RegisterView.as_view(), name="home"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path('accounts/', include('django.contrib.auth.urls')),

    ]
