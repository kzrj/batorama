# Generated by Django 3.2 on 2021-05-31 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_rama_stock_type'),
        ('rawstock', '0003_alter_timberrecord_rama'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timberrecord',
            name='rama',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='timber_records', to='stock.rama'),
        ),
    ]
