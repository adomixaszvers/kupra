from django.contrib import admin
from models import UnitOfMeasure, Recipe, RecipeProduct, RecipeComment, MenuRecipe

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from kupra.models import KupraUser


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class KupraUserInline(admin.StackedInline):
    model = KupraUser
    can_delete = False
    verbose_name = 'KuPRA vartotojai'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (KupraUserInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(UnitOfMeasure)
admin.site.register(Recipe)
admin.site.register(RecipeProduct)
admin.site.register(RecipeComment)
admin.site.register(MenuRecipe)