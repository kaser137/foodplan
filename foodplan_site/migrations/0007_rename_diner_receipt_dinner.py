# Generated by Django 4.2.5 on 2023-10-01 23:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan_site', '0006_rename_diner_price_dinner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receipt',
            old_name='diner',
            new_name='dinner',
        ),
    ]
