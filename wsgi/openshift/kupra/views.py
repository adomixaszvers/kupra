from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from models import Recipe, KupraUser
from django.contrib.auth.decorators import login_required
from forms import RecipeCreateForm, RecipeProductFormSet
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RecipeMixin, self).dispatch(*args, **kwargs)


class RecipeCreateView(RecipeMixin, CreateView):
    form_class = RecipeCreateForm
    template_name = 'test/test.html'

class RecipeListView(ListView):
    model = Recipe
    paginate_by = 1


class RecipeDetailView(DetailView):
    model = Recipe


class RecipeUpdateView(RecipeMixin, UpdateView):
    model = Recipe
    fields = ['name', 'text', 'img', 'time', 'portions']
    template_name = 'test/test.html'

    def get_object(self, queryset=None):
        """Returns the object the view is displaying.

        """

        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get('pk', None)
        queryset = queryset.filter(
            pk=pk,
            user=self.request.user,
        )

        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(u"No %(verbose_name)s found matching the query" %
                          {'verbose_name': queryset.model._meta.verbose_name})

        return obj