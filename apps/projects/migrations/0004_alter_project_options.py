# Generated by Django 5.2.4 on 2025-07-12 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_alter_project_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['id']},
        ),
    ]
