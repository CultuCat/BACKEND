# Generated by Django 4.2.6 on 2023-11-19 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('nom', models.CharField(primary_key=True, serialize=False)),
            ],
        ),
    ]
