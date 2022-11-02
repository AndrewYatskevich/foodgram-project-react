from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    subscriptions = models.ManyToManyField('self', related_name='subscribers')
    favorite = models.ManyToManyField('recipes.Recipe',
                                      related_name='favorite')
    shopping_cart = models.ManyToManyField('recipes.Recipe',
                                           related_name='shopping_cart')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('id',)
