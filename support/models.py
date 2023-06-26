from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=200)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    
class TicketAnswer(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    admin_name = models.CharField(max_length=200, blank=True)
    body = models.TextField(max_length=200)

    def __str__(self):
        return f'{self.ticket}'
