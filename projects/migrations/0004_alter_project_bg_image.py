# Generated by Django 5.0.3 on 2024-03-18 19:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_bg_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='bg_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_bg_img', to='projects.backgroundimage'),
        ),
    ]
