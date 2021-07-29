# Generated by Django 3.2 on 2021-07-06 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        # ('stock', '0007_remove_shift_quota'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lumberrecord',
            options={'ordering': ['lumber__wood_species', 'lumber__lumber_type']},
        ),
        migrations.AddField(
            model_name='sale',
            name='system_fee',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
