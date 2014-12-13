# -*- coding: utf-8 -*-
from django import forms
import account.forms


class SignupForm(account.forms.SignupForm):
    first_name = forms.CharField(max_length=20, label="Vardas")
    last_name = forms.CharField(max_length=20, label="Pavardė")
    img = forms.ImageField(label="Jūsų nuotrauka")
    address = forms.CharField(label="Addresas", widget=forms.Textarea)
    info = forms.CharField(label="Aprašymas", widget=forms.Textarea)