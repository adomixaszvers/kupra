from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from models import Recipe

# Create your views here.

from django.views.generic.edit import CreateView, UpdateView, DeleteView

class RecipeCreateView(CreateView):
    model = Recipe
    success_url = reverse_lazy('home')
