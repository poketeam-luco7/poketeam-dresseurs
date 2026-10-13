from django.urls import path

from .views import HealthView, LoginView, ProfileView, UsersView

urlpatterns = [
    path("users", UsersView.as_view()),           # POST inscription, PUT profil
    path("auth/login", LoginView.as_view()),
    path("auth/profile", ProfileView.as_view()),
    path("health", HealthView.as_view()),
]
