# Generated by Django 5.1.4 on 2025-01-27 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='court',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
