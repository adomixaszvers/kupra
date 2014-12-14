#-*- encoding: utf-8 -*-
from models import Recipe, RecipeProduct, MenuRecipe
from django import forms
from django.forms.models import inlineformset_factory
from datetimewidget.widgets import DateTimeWidget
from datetime import datetime


class RecipeCreateForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['name', 'text', 'img', 'time', 'portions']

RecipeProductFormSet = inlineformset_factory(Recipe, RecipeProduct, extra=3, max_num=20)

class AddRecipeToMenuForm(forms.ModelForm):

    class Meta:
        model = MenuRecipe
        fields = ['date']
        dateTimeOptions = {
            'startDate': datetime.today(),
            'bootstrap_version': 2,
            'usel10n':True
        }
        widgets = {
            #NOT Use localization and set a default format
            'date': DateTimeWidget(bootstrap_version=2, usel10n=True),
        }

class MenuForm(forms.ModelForm):
    class Meta:
        model = MenuRecipe
        fields = ['date', 'recipe']
        dateTimeOptions = {
            'startDate': datetime.today(),
            'bootstrap_version': 2,
            'usel10n':True
        }
        widgets = {
            #NOT Use localization and set a default format
            'date': DateTimeWidget(bootstrap_version=2, usel10n=True),
        }