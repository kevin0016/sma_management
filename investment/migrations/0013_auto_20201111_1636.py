# Generated by Django 3.1.2 on 2020-11-11 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0012_auto_20201111_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundpurchaseandredeem',
            name='max_apply',
            field=models.DecimalField(decimal_places=2, max_digits=18, max_length=20, null=True, verbose_name='单日限额'),
        ),
        migrations.AlterField(
            model_name='fundpurchaseandredeem',
            name='min_apply',
            field=models.DecimalField(decimal_places=2, max_digits=18, max_length=20, null=True, verbose_name='购买起点'),
        ),
    ]
