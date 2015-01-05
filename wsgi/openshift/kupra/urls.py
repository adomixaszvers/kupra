from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from views import (
    RecipeCreateView,
    RecipeListView,
    RecipeDetailView,
    RecipeUpdateView,
    RecipeDeleteView,
    AddRecipeToMenuView,
    MenuRecipeInline,
    produce_recipe,
    RecipeCommentView,
    RecipeCommentListView,
    manage_fridge,
    UnitCreateView,
    UnitListView,
    could_produce_recipe,
    missing_menu_products,
    )
urlpatterns = patterns('',
    # Examples:
    url(r"^recipe/create$", RecipeCreateView.as_view(), name="recipe_create"),
    url(r"^recipes$", RecipeListView.as_view(), name="recipe_list"),
    url(r"^recipe/(?P<pk>\d+)$", RecipeDetailView.as_view(), name="recipe_detail"),
    url(r"^recipe/(?P<pk>\d+)/update$", RecipeUpdateView.as_view(), name="recipe_update"),
    url(r"^recipe/(?P<pk>\d+)/delete$", RecipeDeleteView.as_view(), name="recipe_delete"),
    url(r"^recipe/(?P<menu_recipe_pk>\d+)/produce$", produce_recipe, name="recipe_produce"),
    url(r"^recipe/(?P<recipe_pk>\d+)/comment$", RecipeCommentView.as_view(), name="recipe_comment"),
    url(r"^recipe/(?P<recipe_pk>\d+)/comments$", RecipeCommentListView.as_view(), name="recipe_comments"),
    url(r"^recipe/(?P<menu_recipe_pk>\d+)/could$", could_produce_recipe, name="could_produce_recipe"),
    url(r"^menu/(?P<pk>\d+)/add$", AddRecipeToMenuView.as_view(), name="add_recipe_to_menu"),
    url(r"^menu/missing$", missing_menu_products, name="missing_menu_products"),
    url(r"^fridge$", manage_fridge, name="fridge"),
    url(r"^menu$", MenuRecipeInline.as_view(), name="menu"),
    url(r"^unit/create$", UnitCreateView.as_view(), name="unit_create"),
    url(r"^units$", UnitListView.as_view(), name="unit_list"),
)
