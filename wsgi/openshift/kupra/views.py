from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from models import Recipe
from django.contrib.auth.decorators import login_required
from forms import RecipeCreateForm, RecipeProductFormSet


# Create your views here.

from django.views.generic.edit import (
        CreateView,
        UpdateView,
        DeleteView,
        )
from django.views.generic.list import ListView

class RecipeCreateView(CreateView):
    form_class = RecipeCreateForm
    template_name = 'test/test.html'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        recipeproduct_form = RecipeProductFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  recipeproduct_form=recipeproduct_form,))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        recipeproduct_form = RecipeProductFormSet(self.request.POST)
        if (form.is_valid() and recipeproduct_form.is_valid()):
            return self.form_valid(form, recipeproduct_form)
        else:
            return self.form_invalid(form, recipeproduct_form)

    def form_valid(self, form, recipeproduct_form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        recipeproduct_form.instance = self.object
        recipeproduct_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, recipeproduct_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  recipeproduct_form=recipeproduct_form))

    def get_success_url(self):
        return reverse_lazy('recipe_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RecipeCreateView, self).dispatch(*args, **kwargs)

class RecipeListView(ListView):
    model = Recipe
