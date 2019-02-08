# Generated by Django 2.1 on 2018-08-30 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('katalog', '0002_auto_20180829_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='Svjetiljka',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oib', models.CharField(max_length=50)),
                ('stup', models.DecimalField(decimal_places=1, max_digits=3)),
                ('tip_svjetiljke', models.CharField(max_length=25)),
                ('tip_svjetlosti', models.CharField(max_length=25)),
                ('snaga', models.IntegerField()),
                ('klasa_povrsine', models.CharField(max_length=10)),
                ('x_koordinata', models.CharField(max_length=15)),
                ('y_koordinata', models.CharField(max_length=15)),
            ],
        ),
    ]
