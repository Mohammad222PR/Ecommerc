# Generated by Django 4.2.2 on 2023-06-26 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticketanswer',
            old_name='name',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='blogs/'),
        ),
    ]
