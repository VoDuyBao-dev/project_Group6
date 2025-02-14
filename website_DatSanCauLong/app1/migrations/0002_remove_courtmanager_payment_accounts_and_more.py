# Generated by Django 5.1.6 on 2025-02-14 14:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courtmanager',
            name='payment_accounts',
        ),
        migrations.AddField(
            model_name='paymentaccount',
            name='court_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_accounts', to='app1.courtmanager'),
        ),
        migrations.AlterField(
            model_name='courtmanager',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
