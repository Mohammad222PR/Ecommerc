from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=200)
    complete = models.BooleanField(default=False)
    images = models.ImageField(upload_to='blogs/', null = True)

    def __str__(self):
        return self.user
class TicketAnswer(models.Model):
    ticket = models.ForeignKey(Ticket)
    name = models.ForeignKey(User)
    body = models.TextField(max_length=200)