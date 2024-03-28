# Generated by Django 5.0.3 on 2024-03-28 00:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='publish_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]