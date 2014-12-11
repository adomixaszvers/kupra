from models import Recipe, RecipeProduct
from django import forms
from django.forms.models import inlineformset_factory

class RecipeCreateForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['name', 'text', 'img']

RecipeProductFormSet = inlineformset_factory(Recipe, RecipeProduct, extra=10, max_num=1)
