# Generated by Django 5.0.3 on 2024-03-19 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_rename_depatment_task_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='members',
        ),
        migrations.AddField(
            model_name='task',
            name='workers',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
