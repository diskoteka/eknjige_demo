# Generated by Django 2.1 on 2018-08-31 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('katalog', '0004_auto_20180831_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='omm',
            name='brojilo',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='omm',
            name='sifra',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='svjetiljka',
            name='snaga',
            field=models.IntegerField(),
        ),
    ]
