# Generated by Django 3.1.2 on 2020-12-03 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0034_auto_20201203_1024'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockDailyQuote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('closeprice', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='收盘价')),
                ('prevcloseprice', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='收盘价')),
                ('date', models.DateField(verbose_name='交易日')),
                ('secucode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investment.stock', verbose_name='股票代码')),
            ],
            options={
                'verbose_name': '股票日行情',
                'verbose_name_plural': '股票日行情',
                'db_table': 'sma_stock_daily_quote',
                'unique_together': {('secucode', 'date')},
            },
        ),
    ]
