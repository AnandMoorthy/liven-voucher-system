# Generated by Django 5.0 on 2023-12-10 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_customerwallet_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerwallet',
            name='redeemed',
            field=models.BooleanField(default=False),
        ),
    ]
