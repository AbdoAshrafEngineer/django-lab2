from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib import messages

def register(req):
    if req.method == 'POST':
        form = RegisterForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user = form.save()
            messages.success(req, "Registration successful. Please log in.")

            return redirect("login")
        else:
            # Add form errors to messages for display in template
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(req, f"{field}: {error}")
    else:
        form = RegisterForm()
    return render(req, 'accounts/register.html', {'f': form})

