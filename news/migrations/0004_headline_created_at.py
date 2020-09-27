# Generated by Django 3.1.1 on 2020-09-26 09:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_headline'),
    ]

    operations = [
        migrations.AddField(
            model_name='headline',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
