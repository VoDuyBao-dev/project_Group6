# Generated by Django 5.1.4 on 2025-02-03 05:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_remove_badmintonhall_systemadmin_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='courtmanager',
            name='Thongtintaikhoan',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='court_manager', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='revenuereport',
            name='generated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='systemadmin',
            name='Thongtintaikhoan',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='system_admin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customer',
            name='Thongtintaikhoan',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='courtstaff',
            name='Thongtintaikhoan',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='court_staff', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
