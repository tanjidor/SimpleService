# Generated by Django 3.2 on 2021-04-12 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serpis', '0002_auto_20210411_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderan',
            name='tgl_keluar',
            field=models.DateField(blank=True, null=True),
        ),
    ]