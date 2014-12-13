from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from views import RecipeCreateView, RecipeListView, RecipeDetailView, RecipeUpdateView

urlpatterns = patterns('',
    # Examples:
    url(r"^recipe/create$", RecipeCreateView.as_view(), name="recipe_create"),
    url(r"^recipes$", RecipeListView.as_view(), name="recipe_list"),
    url(r"^recipe/(?P<pk>\d+)$", RecipeDetailView.as_view(), name="recipe_detail"),
    url(r"^recipe/(?P<pk>\d+)/update$", RecipeUpdateView.as_view(), name="recipe_update"),
)
