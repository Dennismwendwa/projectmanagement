# Generated by Django 5.0.3 on 2024-03-19 18:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_project_slug'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('depatment', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('deadline', models.DateTimeField()),
                ('checklist', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
            options={
                'verbose_name': 'task',
                'verbose_name_plural': 'tasks',
                'ordering': ('deadline',),
            },
        ),
    ]
