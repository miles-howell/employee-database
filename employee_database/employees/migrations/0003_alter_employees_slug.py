# Generated by Django 5.2 on 2025-04-24 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_alter_employees_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
