# Generated by Django 5.0 on 2023-12-10 09:31

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zipcode', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='restaurantbranches',
            name='unique_id',
            field=models.CharField(default=uuid.uuid4, max_length=20, unique=True),
        )
    ]
