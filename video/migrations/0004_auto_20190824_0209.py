# Generated by Django 2.1.1 on 2019-08-24 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0003_auto_20190823_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videouser',
            name='number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
