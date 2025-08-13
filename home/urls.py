from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("profile/", views.profile, name="profile"),  # target of LOGIN_REDIRECT_URL
]
