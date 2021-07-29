# Generated by Django 3.2 on 2021-07-06 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0008_auto_20210706_1522'),
        ('accounts', '0003_account_is_boss'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='can_see_rama_stock',
            field=models.ManyToManyField(related_name='accounts_can_see_stock', to='stock.Rama'),
        ),
    ]
