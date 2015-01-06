# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from models import Recipe, KupraUser, UserProduct, RecipeComment, MissingProduct
from django.contrib.auth.decorators import login_required
from forms import (
    RecipeCreateForm,
    RecipeProductFormSet,
    AddRecipeToMenuForm,
    MenuForm,
    RecipeCommentForm,
    UserProductForm,
    )
from django.http import Http404
from extra_views import InlineFormSet, UpdateWithInlinesView, InlineFormSetView
from models import RecipeProduct, MenuRecipe, UnitOfMeasure
from django.db.models import ProtectedError
from django.views.generic import FormView
from django.contrib.auth.models import User
from django.db.models import Q
from django.template import RequestContext
from collections import defaultdict
from django.forms.models import inlineformset_factory
from django.db.models import Sum


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
    paginate_by = 10

    def get_queryset(self):
        if not self.request.user.id is None:
            return Recipe.objects.filter(
                Q(user=self.request.user) | Q(private=False)
            )
        else:
            return Recipe.objects.filter(private=False)


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(RecipeDetailView, self).get_context_data(**kwargs)
        recipe = context['recipe']
        # Add in a QuerySet of all the books
        context['products'] = RecipeProduct.objects.filter(recipe=recipe)
        return context


class RecipeProductInline(InlineFormSet):
    model = RecipeProduct

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class GalimaPagamintiView(LoginRequiredMixin, ListView):
    model = Recipe
    paginate_by = 10
    template_name="kupra/recipe_list.html"

    def get_queryset(self):
        user = self.request.user
        queryset = Recipe.objects.filter(
                Q(user=self.request.user) | Q(private=False)
            )
        recipes_to_exclude = list()
        for recipe in queryset:
            exclude = False
            for product in recipe.recipeproduct_set.all():
                user_products = UserProduct.objects.filter(
                    user=user,
                    name=product.name,
                    unit=product.unit,
                    )
                if not user_products.exists:
                    exclude = True
                    break
                user_quantity = user_products.aggregate(
                    Sum('quantity')).values()[0]
                if product.quantity > user_quantity:
                    exclude = True
                    break
            if exclude:
                recipes_to_exclude.append(recipe)
        for recipe in recipes_to_exclude:
            queryset = queryset.exclude(pk=recipe.pk)
        return queryset


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
    extra = 0


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
            return render_to_response(
                'kupra/error.html',
                {'error': u'Negalima, nes receptas įtrauktas į valgiaraštį'},
                RequestContext(self.request),
                )

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


class MenuRecipeInline(LoginRequiredMixin, InlineFormSetView):
    model = User
    inline_model = MenuRecipe
    template_name = 'kupra/menu.html'
    form_class = MenuForm
    extra = 0

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)


@login_required
def produce_recipe(request, menu_recipe_pk):
    menu_recipe = get_object_or_404(MenuRecipe, pk=menu_recipe_pk)
    recipe = menu_recipe.recipe
    ratio = menu_recipe.portions * 1.0 / recipe.portions
    user_products = request.user.userproduct_set.all()
    recipe_products = recipe.recipeproduct_set.all()
    is_enough = True
    required = list()
    to_save = list()
    for recipe_product in recipe_products:
        unit = recipe_product.unit
        name = recipe_product.name
        quantity = recipe_product.quantity * ratio
        try:
            user_product = user_products.get(name=name, unit=unit)
            user_quantity = user_product.quantity
            user_product.quantity -= quantity
            to_save.append(user_product)
        except UserProduct.DoesNotExist:
            user_quantity = 0
        if user_quantity < quantity:
            is_enough = False
            required.append(
                {'name': name,
                    'unit': unit.name,
                    'quantity': quantity - user_quantity
                    })
            continue
    if is_enough:
        for user_product in to_save:
            user_product.save()
        return render_to_response(
            'kupra/recipe_produced.html',
            {'recipe': recipe},
            RequestContext(request),
            )
    else:
        return render_to_response(
            'kupra/recipe_required_products.html',
            {'products': required},
            RequestContext(request),
            )


def missing_products(user, menu_recipes):
    quantities = defaultdict(dict)
    for menu_recipe in menu_recipes:
        recipe = menu_recipe.recipe
        ratio = menu_recipe.portions * 1.0 / recipe.portions
        for product in recipe.recipeproduct_set.all():
            name = product.name
            unit = product.unit.pk
            quantity = product.quantity * ratio
            if name in quantities:
                if unit in quantities[name]:
                    quantities[name][unit] = quantities[name][unit] + quantity
            else:
                quantities[name][unit] = quantity
    user_products = UserProduct.objects.filter(user=user)
    is_enough = True
    required = list()
    to_save = list()
    for name in quantities.keys():
        for unit in quantities[name].keys():
            quantity = quantities[name][unit]
            try:
                unitobj = UnitOfMeasure.objects.get(pk=unit)
                user_product = user_products.get(name=name, unit=unitobj)
                user_quantity = user_product.quantity
                user_product.quantity -= quantity
                to_save.append(user_product)
            except UserProduct.DoesNotExist:
                user_quantity = 0
            if user_quantity < quantity:
                is_enough = False
                required.append(
                    {'name': name,
                    'unit': unitobj.name,
                    'quantity': quantity - user_quantity
                    })
                continue
    if is_enough:
        return None
    else:
        return required


@login_required
def could_produce_recipe(request, menu_recipe_pk):
    menu_recipe = get_object_or_404(MenuRecipe, pk=menu_recipe_pk)
    required = missing_products(request.user, (menu_recipe,))
    return render_to_response(
            'kupra/recipe_required_products.html',
            {
                'products': required,
                'menu_recipe': menu_recipe,
            },
            RequestContext(request),
            )


@login_required
def missing_menu_products(request):
    menu_recipes = MenuRecipe.objects.filter(user=request.user)
    required = missing_products(request.user, menu_recipes)
    return render_to_response(
            'kupra/menu_required_products.html',
            {
                'products': required,
            },
            RequestContext(request),
            )


class RecipeCommentView(LoginRequiredMixin, FormView):
    form_class = RecipeCommentForm
    template_name = 'kupra/comment.html'
    success_url = reverse_lazy('recipe_list')

    def form_valid(self, form):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_pk'])
        score = form.cleaned_data['score']
        comment = form.cleaned_data['comment']
        try:
            obj = RecipeComment.objects.get(
                user=user,
                recipe=recipe,
                )
            obj.score = form.cleaned_data['score']
            obj.comment = form.cleaned_data['comment']
        except RecipeComment.DoesNotExist:
            obj = RecipeComment.objects.create(
                recipe=recipe,
                comment=comment,
                score=score,
                user=user,
                )
        obj.save()
        return FormView.form_valid(self, form)


class RecipeCommentListView(ListView):
    model = RecipeComment
    paginate_by = 20

    def get_queryset(self):
        recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_pk'])
        comments = RecipeComment.objects.filter(recipe=recipe)
        return comments


@login_required
def manage_fridge(request):
    UserProductFormSet = inlineformset_factory(
        User,
        UserProduct,
        form=UserProductForm,
        extra=0,
        )
    if request.method == 'POST':
        formset = UserProductFormSet(
            request.POST,
            request.FILES,
            instance=request.user)
        if formset.is_valid():
            products = formset.save(commit=False)
            for product in products:
                product.user = request.user
                product.save()
            for obj in formset.deleted_objects:
                obj.delete()
    else:
        formset = UserProductFormSet(
            instance=request.user
            )
    return render_to_response("kupra/fridge_form.html", {
        "formset": formset,
    }, RequestContext(request))


@login_required
def save_missing_products(request):
    menu_recipes = MenuRecipe.objects.filter(user=request.user)
    required = missing_products(request.user, menu_recipes)
    MissingProduct.objects.filter(user=request.user).delete()
    for values in required:
        unit = get_object_or_404(UnitOfMeasure, name=values['unit'])
        missing_product = MissingProduct(
            user=request.user,
            name=values['name'],
            unit=unit,
            quantity=values['quantity'],
            )
        missing_product.save()
    return redirect('missing_products')


@login_required
def manage_missing_products(request):
    MissingProductFormSet = inlineformset_factory(
        User,
        MissingProduct,
        form=UserProductForm,
        extra=0,
        )
    if request.method == 'POST':
        formset = MissingProductFormSet(
            request.POST,
            request.FILES,
            instance=request.user)
        if formset.is_valid():
            products = formset.save(commit=False)
            for product in products:
                product.user = request.user
                product.save()
            for obj in formset.deleted_objects:
                obj.delete()
    else:
        formset = MissingProductFormSet(
            instance=request.user
            )
    return render_to_response("kupra/missing_form.html", {
        "formset": formset,
    }, RequestContext(request))


@login_required
def add_missing_to_fridge(request):
    missing_products = MissingProduct.objects.filter(user=request.user)
    for missing_product in missing_products:
        user_product = UserProduct(
            user=missing_product.user,
            name=missing_product.name,
            unit=missing_product.unit,
            quantity=missing_product.quantity
            )
        user_product.save()
    missing_products.delete()
    return redirect('fridge')


class UnitCreateView(LoginRequiredMixin, CreateView):
    model = UnitOfMeasure
    success_url = reverse_lazy('unit_list')

class UnitListView(LoginRequiredMixin, ListView):
    model = UnitOfMeasure