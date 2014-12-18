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
    produce_all_recipes,
    RecipeCommentView,
    RecipeCommentListView,
    )
urlpatterns = patterns('',
    # Examples:
    url(r"^recipe/create$", RecipeCreateView.as_view(), name="recipe_create"),
    url(r"^recipes$", RecipeListView.as_view(), name="recipe_list"),
    url(r"^recipe/(?P<pk>\d+)$", RecipeDetailView.as_view(), name="recipe_detail"),
    url(r"^recipe/(?P<pk>\d+)/update$", RecipeUpdateView.as_view(), name="recipe_update"),
    url(r"^recipe/(?P<pk>\d+)/delete$", RecipeDeleteView.as_view(), name="recipe_delete"),
    url(r"^recipe/(?P<recipe_pk>\d+)/produce$", produce_recipe, name="recipe_produce"),
    url(r"^recipe/(?P<recipe_pk>\d+)/comment$", RecipeCommentView.as_view(), name="recipe_comment"),
    url(r"^recipe/(?P<recipe_pk>\d+)/comments$", RecipeCommentListView.as_view(), name="recipe_comments"),
    url(r"^menu/(?P<pk>\d+)/add$", AddRecipeToMenuView.as_view(), name="add_recipe_to_menu"),
    url(r"^menu$", MenuRecipeInline.as_view(), name="menu"),
    url(r"^menu/produce$", produce_all_recipes, name="menu-produce"),
)
