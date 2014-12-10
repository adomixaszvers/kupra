from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from views import RecipeCreateView

urlpatterns = patterns('',
    # Examples:
    url(r"^recipe/create$", RecipeCreateView.as_view(), name="recipe_create"),
)
