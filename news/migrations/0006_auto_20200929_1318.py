# Generated by Django 3.1.1 on 2020-09-29 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20200929_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headline',
            name='title',
            field=models.TextField(),
        ),
    ]
