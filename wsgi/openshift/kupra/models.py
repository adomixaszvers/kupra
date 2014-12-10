from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from uuid_upload_path import upload_to

# Create your models here.

class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=20)
    quantity = models.FloatField()
    unit = models.ForeignKey(UnitOfMeasure, on_delete=models.PROTECT)

    class Meta:
        abstract = True

    def __unicode__(self):
        name = self.name
        quantity = self.quantity
        unit = self.unit
        return u"{name}: {quantity} {unit}".format(
            name=name,
            quantity=quantity,
            unit=unit
            )
class UserProduct(Product):
    user = models.ForeignKey(User)

    def __unicode__(self):
        user = self.user
        string = super(UserProduct, self).__unicode__()
        return _(u"{user}'s {string}".format(user=user, string=string))

class RecipeProduct(Product):
    recipe = models.ForeignKey('Recipe')

class Recipe(models.Model):
    name = models.CharField(max_length=20)
    text = models.TextField()
    img = models.ImageField(upload_to=upload_to)

    def __unicode__(self):
        return self.name
