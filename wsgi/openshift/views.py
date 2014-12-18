import os
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, Http404
import forms
import account.views
from kupra.models import KupraUser


def home(request):
    #return render_to_response('home/home.html')
    return reverse_lazy('recipe_list')


class SignupView(account.views.SignupView):

    form_class = forms.SignupForm

    def after_signup(self, form):
        self.create_profile(form)
        super(SignupView, self).after_signup(form)

    def create_profile(self, form):
        user = self.created_user
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        img = form.cleaned_data["img"]
        address = form.cleaned_data["address"]
        info = form.cleaned_data["info"]
        kuprauser = KupraUser.objects.create_kuprauser(user, img, address, info)
        user.kuprauser = kuprauser
        user.save()
