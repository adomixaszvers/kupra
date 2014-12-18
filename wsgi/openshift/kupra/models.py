# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from uuid_upload_path import upload_to
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction


# Create your models here.

class KupraUserManager(models.Manager):

    def create_kuprauser(self, user, img, address, info):
        kuprauser = self.create(user=user, img=img, address=address, info=info)
        return kuprauser


class KupraUser(models.Model):
    user = models.OneToOneField(User, verbose_name=u'Vartotojas')
    img = models.ImageField(
        upload_to=upload_to,
        verbose_name="uProfilio nuotrauka"
    )
    address = models.TextField(verbose_name=u"Adresas")
    info = models.TextField(verbose_name=u"Aprašymas")
    objects = KupraUserManager()

    class Meta:
        verbose_name = u'KuPRA vartotojas'
        verbose_name_plural = u'KuPRA vartotojai'


class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'Pavadinimas')

    class Meta:
        verbose_name = u'Matavimo vienetas'
        verbose_name_plural = u'Matavimo vienetai'

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'Pavadinimas')
    quantity = models.FloatField(verbose_name=u'Kiekis')
    unit = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.PROTECT,
        verbose_name=u'Matavimo vienetas'
        )

    class Meta:
        abstract = True
        verbose_name = u'Ingredientas'
        verbose_name_plural = u'Ingredientai'

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
    user = models.ForeignKey(User, verbose_name=u'Vartotojas')

    class Meta:
        verbose_name = u'Vartotojo produktas'
        verbose_name_plural = u'Vartotojo produktai'


@receiver(post_save, sender=UserProduct)
@transaction.atomic
def user_product_unique(sender, **kwargs):
    if not kwargs.get('created'):
        return
    product = kwargs.get('instance')
    name = product.name
    user = product.user
    unit = product.unit
    q = UserProduct.objects.filter(name=name, user=user, unit=unit)
    if q.count() <= 1:
        return
    quantity = q.aggregate(models.Sum('quantity')).values()[0]
    if q.count() == 0:
        return
    product = q.first()
    q = q.exclude(pk=product.pk)
    q.delete()
    product.quantity = quantity
    product.save()
    return


@receiver(post_save, sender=UserProduct)
def recipe_product_zero(sender, **kwargs):
    product = kwargs['instance']
    if product.quantity > 0:
        return
    else:
        product.delete()


class RecipeProduct(Product):
    recipe = models.ForeignKey('Recipe', verbose_name=u'Receptas')

    class Meta:
        verbose_name = u'Recepto ingredientas'
        verbose_name_plural = u'Recepto ingredientai'


@receiver(post_save, sender=RecipeProduct)
@transaction.atomic
def recipe_product_unique(sender, **kwargs):
    if not kwargs.get('created'):
        return
    product = kwargs.get('instance')
    name = product.name
    recipe = product.recipe
    unit = product.unit
    q = RecipeProduct.objects.filter(name=name, recipe=recipe, unit=unit)
    if q.count() <= 1:
        return
    quantity = q.aggregate(models.Sum('quantity')).values()[0]
    if q.count() == 0:
        return
    product = q[0]
    q = q.exclude(pk=product.pk)
    q.delete()
    product.quantity = quantity
    product.save()
    return


@receiver(post_save, sender=RecipeProduct)
def recipe_product_zero(sender, **kwargs):
    product = kwargs['instance']
    if product.quantity > 0:
        return
    else:
        product.delete()


class RecipeComment(models.Model):
    CHOICES = ((x, x) for x in range(1, 11))
    recipe = models.ForeignKey('kupra.Recipe', verbose_name=u'Receptas')
    user = models.ForeignKey(User, verbose_name=u'Vartotojas')
    score = models.IntegerField(choices=CHOICES, verbose_name=u'Įvertinimas')
    comment = models.TextField(verbose_name=u'Komentaras')

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = u'Recepto komentaras'
        verbose_name_plural = u'Recepto komentarai'

    def __unicode__(self):
        score = self.score
        user = self.user
        return u"Vartotojas: {}, įvertinimas {}".format(user, score)


class Recipe(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'Pavadinimas')
    text = models.TextField(verbose_name=u'Aprašymas')
    img = models.ImageField(
        upload_to=upload_to,
        default='default.jpg',
        verbose_name=u'Nuotrauka'
        )
    user = models.ForeignKey(User, null=True, verbose_name=u'Vartotojas')
    portions = models.IntegerField(verbose_name=u'Porcijų kiekis')
    time = models.CharField(max_length=20, verbose_name=u'Paruošimo laikas')
    private = models.BooleanField(default=False, verbose_name=u'Privatus')
    avgscore = models.FloatField(default=0, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Receptas'
        verbose_name_plural = u'Receptai'
        ordering = ['-avgscore', ]


def update_avgscore(sender, **kwargs):
    comment = kwargs['instance']
    recipe = comment.recipe
    comments = RecipeComment.objects.filter(recipe=recipe)
    avgscore = comments.aggregate(models.Avg('score')).values()[0]
    recipe.avgscore = avgscore
    recipe.save()


post_save.connect(update_avgscore, sender=RecipeComment)
post_delete.connect(update_avgscore, sender=RecipeComment)


class MenuRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.PROTECT,
        verbose_name=u'Receptas'
        )
    date = models.DateTimeField(verbose_name=u'Data')
    user = models.ForeignKey(User, verbose_name=u'Vartotojas')

    class Meta:
        verbose_name = u'Valgiaraščio receptas'
        verbose_name_plural = u'Valgiaraščio receptai'

    def __unicode__(self):
        recipe = self.recipe.name
        date = self.date
        return u"Receptas: {}\nData: {}".format(recipe, date)
