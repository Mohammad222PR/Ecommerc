# Generated by Django 4.2.2 on 2023-06-26 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0003_remove_ticket_images_ticket_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='answer',
        ),
    ]