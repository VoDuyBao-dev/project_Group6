# Generated by Django 5.1.4 on 2025-02-06 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_revenuereport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentaccount',
            name='accountHolder',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='paymentaccount',
            name='accountNumber',
            field=models.CharField(max_length=20),
        ),
    ]
