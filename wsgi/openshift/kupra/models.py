# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from uuid_upload_path import upload_to
from django.conf import settings

# Create your models here.

class KupraUserManager(models.Manager):

    def create_kuprauser(self, user, img, address, info):
        kuprauser = self.create(user=user, img=img, address=address, info=info)
        return kuprauser


class KupraUser(models.Model):
    user = models.OneToOneField(User)
    img = models.ImageField(
        upload_to=upload_to,
        verbose_name="Profilio nuotrauka"
    )
    address = models.TextField(verbose_name="Adresas")
    info = models.TextField(verbose_name="Aprašymas")
    objects = KupraUserManager()


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        user = self.user
        string = super(UserProduct, self).__unicode__()
        return _(u"{user}'s {string}".format(user=user, string=string))


class RecipeProduct(Product):
    recipe = models.ForeignKey('Recipe')


class Recipe(models.Model):
    name = models.CharField(max_length=20)
    text = models.TextField()
    img = models.ImageField(upload_to=upload_to, default='default.jpg')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    def __unicode__(self):
        return self.name
