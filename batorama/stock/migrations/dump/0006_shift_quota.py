# Generated by Django 3.2 on 2021-05-31 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rawstock', '0010_quota'),
        ('stock', '0005_rama_stock_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='quota',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shifts', to='rawstock.quota'),
        ),
    ]
