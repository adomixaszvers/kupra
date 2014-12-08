import os
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, Http404

def home(request):
    return render_to_response('home/home.html')

def registruotis(request):
    return render_to_response('home/registruotis.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_page = reverse_lazy("home")
                return HttpResponseRedirect(next_page)
            else:
                # Return a 'disabled account' error message
                return render_to_response('home/disabled.html')
        else:
            # Return an 'invalid login' error message.
            return render_to_response('home/invalid.html')
    else:
        return render(request,'auth/login.html')
