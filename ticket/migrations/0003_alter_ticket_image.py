# Generated by Django 4.2.6 on 2023-12-21 15:17

from django.db import migrations, models
import ticket.models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.ImageField(default=ticket.models.get_random_image, upload_to=''),
        ),
    ]