# Generated by Django 5.0 on 2023-12-10 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_restaurantcity_alter_restaurantbranches_unique_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantbranches',
            name='unique_id',
            field=models.CharField(default='6ba7c412', max_length=20, unique=True),
        ),
    ]
