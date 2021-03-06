# Generated by Django 2.2.1 on 2019-05-27 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Feature')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=50, verbose_name='Brand')),
                ('trading_name', models.CharField(max_length=150, null=True, verbose_name='Trading Name')),
                ('phone', models.CharField(max_length=50, null=True, verbose_name='Phone')),
                ('address', models.CharField(max_length=250, verbose_name='Address')),
                ('suburb', models.CharField(max_length=80, verbose_name='Location')),
                ('latitude', models.FloatField(verbose_name='Latitude')),
                ('longitude', models.FloatField(verbose_name='Longitude')),
                ('features', models.ManyToManyField(to='fuelprice.Feature', verbose_name='Features')),
            ],
            options={
                'unique_together': {('brand', 'address', 'suburb')},
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('price', models.FloatField(verbose_name='Price')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='fuelprice.Location', verbose_name='Location')),
            ],
        ),
    ]
