# Generated by Django 2.2.1 on 2019-06-03 08:07

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('symbol', models.CharField(blank=True, max_length=1, null=True, verbose_name='Symbol')),
                ('is_default', models.BooleanField(default=False, help_text='Make this the default currency.', verbose_name='Default')),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
                'ordering': ('code',),
            },
        ),
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('rate', models.DecimalField(decimal_places=6, max_digits=12, verbose_name='Rate')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='Created')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='currency_rates.Currency')),
            ],
            options={
                'verbose_name': 'Exchange rate',
                'verbose_name_plural': 'Exchange rates',
                'ordering': ('-date', 'currency__code'),
                'unique_together': {('currency', 'date')},
            },
        ),
    ]
