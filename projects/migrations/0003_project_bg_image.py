# Generated by Django 5.0.3 on 2024-03-18 19:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_backgroundimage_alter_project_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='bg_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_bg_img', to='projects.backgroundimage'),
        ),
    ]