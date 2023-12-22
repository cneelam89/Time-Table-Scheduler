from django.shortcuts import render
from . forms import SignUpForm,LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib import messages

def home (request):
    return render(request, 'home.html')



# register
def user_register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                return HttpResponseRedirect('/accounts/login/')
        else:
            form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    else:
        return HttpResponseRedirect('/')



# Login
def user_login(request):
 if not request.user.is_authenticated:
  if request.method == "POST":
   form = LoginForm(request=request, data=request.POST)
   if form.is_valid():
    uname = form.cleaned_data['username']
    upass = form.cleaned_data['password']
    user = authenticate(username=uname, password=upass)
    if user is not None:
     login(request, user)
     messages.success(request, 'Logged in Successfully !!')
     return HttpResponseRedirect('/')
  else:
   form = LoginForm()
  return render(request, 'login.html', {'form':form})
 else:
  return HttpResponseRedirect('/')



# Logout
def user_logout(request):
 logout(request)
 return HttpResponseRedirect('/')
