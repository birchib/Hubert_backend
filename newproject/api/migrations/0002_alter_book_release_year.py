# Generated by Django 5.1.3 on 2024-11-20 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='release_year',
            field=models.CharField(max_length=255),
        ),
    ]