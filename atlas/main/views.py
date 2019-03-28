from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Subheading
from django.contrib.auth.forms import AuthenticationForm
from .forms import ExtendedUserCreationForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.

def homepage(request):
    return render(request=request,
                  template_name="main/home.html",
                  context={"subheadings": Subheading.objects.all})


def register(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid:
            user = form.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            messages.success(request, "New account created: {}".format(username))

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.info(request, "You are now logged in as: {}".format(username))

            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
    else:
        form = ExtendedUserCreationForm()
        profile_form = ProfileForm()

        context = {'form': form, 'profile_form': profile_form}
        return render(request, "main/register.html", context)

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "You are now logged in as: {}".format(username))
                return redirect("main:homepage")
            else:
                messages.info(request, "Invalid username or password")
        else:
            messages.info(request, "You did not fill out the form correctly!")


    form = AuthenticationForm()
    return render(request,
                  "main/login.html",
                  {"form":form})