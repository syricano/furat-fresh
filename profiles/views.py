from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from .forms import UserForm, UserProfileForm

@login_required
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and form.is_valid():
            user_form.save()
            form.save()
            messages.success(request, "Profile updated")
            return redirect("profiles:profile")
    else:
        user_form = UserForm(instance=request.user)
        form = UserProfileForm(instance=profile)

    return render(request, "profiles/profile.html", {
        "user_form": user_form,
        "form": form,
        "orders": None,
    })
