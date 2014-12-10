from django.contrib import admin
from models import UnitOfMeasure, Recipe, RecipeProduct

# Register your models here.

admin.site.register(UnitOfMeasure)
admin.site.register(Recipe)
admin.site.register(RecipeProduct)
