from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib import messages

def index(request):
    return render(request, "home/index.html")

def about(request):
    return render(request, "pages/about.html")

def contact(request):
    return render(request, "pages/contact.html")

@login_required
def profile(request):
    return render(request, "account/profile.html")

def update_profile(request):
    # ...
    messages.success(request, _("Profile updated successfully"))
