# Generated by Django 3.2.3 on 2021-05-27 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0061_auto_20210322_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='security_deposit',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=18, verbose_name='存出保证金'),
        ),
        migrations.AddField(
            model_name='holding',
            name='trade_market',
            field=models.IntegerField(default=6, verbose_name='交易市场'),
        ),
    ]
