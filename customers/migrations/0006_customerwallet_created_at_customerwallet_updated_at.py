# Generated by Django 5.0 on 2023-12-10 21:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_customerwallet_redeemed'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerwallet',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customerwallet',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]
