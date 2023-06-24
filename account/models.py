from django.db import models
from django.contrib.auth.models import User
from store.models import Customer

class AccountManager(models.Manager):
    def create_account(self, username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        return user

    def create_customer(self, user, name, email):
        customer = Customer.objects.create(user=user, name=name, email=email)
        return customer
# Create your models here.
