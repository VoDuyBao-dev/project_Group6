# Generated by Django 5.1.4 on 2025-02-06 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_alter_court_image_alter_court_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='court',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='app1/static/app1/images'),
        ),
    ]
