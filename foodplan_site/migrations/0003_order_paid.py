# Generated by Django 4.2.5 on 2023-09-29 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan_site', '0002_order_classic_order_keto_order_lowcarb_order_vegan_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='оплачен'),
        ),
    ]
