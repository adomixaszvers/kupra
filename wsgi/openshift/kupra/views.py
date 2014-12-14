# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from models import Recipe, KupraUser
from django.contrib.auth.decorators import login_required
from forms import RecipeCreateForm, RecipeProductFormSet, AddRecipeToMenuForm, MenuForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from extra_views import InlineFormSet, CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetView
from extra_views.generic import GenericInlineFormSet
from models import RecipeProduct, MenuRecipe
import pdb
from django.db.models import ProtectedError
from django.views.generic import FormView
from django.contrib.auth.models import User


# Create your views here.

from django.views.generic.edit import (
        CreateView,
        UpdateView,
        DeleteView,
        )
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

class KupraUserUpdateView(UpdateView):
    model = KupraUser
    fields = ['address', 'info', 'img']
    template_name = 'account/private_update.html'

    def get_object(self):
        return get_object_or_404(KupraUser, pk=self.request.user.kuprauser.pk)

    def get_success_url(self):
        return reverse_lazy('account_private')


class RecipeListView(ListView):
    model = Recipe
    paginate_by = 1


class RecipeDetailView(DetailView):
    model = Recipe


class RecipeProductInline(InlineFormSet):
    model = RecipeProduct

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class OwnerMixin(object):
    def get_object(self, queryset=None):
        obj = super(OwnerMixin,self).get_object(queryset)
        if obj.user != self.request.user:
            raise Http404
        return obj

class RecipeMixin(object):
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
        recipeproduct_form = RecipeProductFormSet(self.request.POST,)
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


class RecipeCreateView(LoginRequiredMixin, RecipeMixin, CreateView):
    form_class = RecipeCreateForm
    template_name = 'test/test.html'

class RecipeUpdateView(LoginRequiredMixin,OwnerMixin,UpdateWithInlinesView):
    model = Recipe
    inlines = [RecipeProductInline, ]
    form_class = RecipeCreateForm


    def get_success_url(self):
        return reverse_lazy('recipe_list')


class RecipeDeleteView(LoginRequiredMixin, OwnerMixin, DeleteView):
    model = Recipe

    def get_success_url(self):
        return reverse_lazy('recipe_list')

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render_to_response('kupra/error.html', {'error': u'Receptas įtrauktas į valgiaraštį'})

class AddRecipeToMenuView(LoginRequiredMixin, FormView):
    form_class = AddRecipeToMenuForm
    template_name = 'kupra/add_recipe_menu.html'
    success_url = reverse_lazy('menu')
    def form_valid(self, form):
        menu_recipe = form.save(commit=False)
        menu_recipe.user = self.request.user
        menu_recipe.recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        menu_recipe.save()
        return super(AddRecipeToMenuView, self).form_valid(form)

class MenuRecipeInline(InlineFormSetView):
    model = User
    inline_model = MenuRecipe
    template_name = 'kupra/menu.html'
    form_class = MenuForm
    extra = 0
    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)