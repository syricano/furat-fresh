from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "core_app/home.html")

def about(request):
    return render(request, "pages/about.html")

def contact(request):
    return render(request, "pages/contact.html")

@login_required
def profile(request):
    return render(request, "account/profile.html")
