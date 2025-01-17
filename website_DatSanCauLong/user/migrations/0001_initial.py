# Generated by Django 5.1.4 on 2025-01-17 04:17

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourtBranch',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CourtManager',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Court',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('hourly_rate_fixed', models.DecimalField(decimal_places=2, max_digits=10)),
                ('hourly_rate_daily', models.DecimalField(decimal_places=2, max_digits=10)),
                ('hourly_rate_flexible', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time_slots', models.JSONField(default=dict)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courts', to='user.courtbranch')),
            ],
        ),
        migrations.AddField(
            model_name='courtbranch',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='user.courtmanager'),
        ),
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('check_in_time', models.DateTimeField(auto_now_add=True)),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='check_ins', to='user.court')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='check_ins', to='user.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('booking_type', models.CharField(choices=[('fixed', 'Fixed'), ('daily', 'Daily'), ('flexible', 'Flexible')], max_length=20)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('total_hours', models.FloatField(blank=True, null=True)),
                ('payment_status', models.BooleanField(default=False)),
                ('is_canceled', models.BooleanField(default=False)),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='user.court')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='user.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], max_length=20)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='user.booking')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('guest', 'Guest'), ('customer', 'Customer'), ('court_manager', 'Court Manager'), ('court_staff', 'Court Staff'), ('admin', 'System Admin')], default='guest', max_length=20)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_user_set', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_user_set', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SystemAdmin',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='system_admin', to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='RevenueReport',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('total_revenue', models.DecimalField(decimal_places=2, max_digits=15)),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='revenue_reports', to='user.courtbranch')),
                ('generated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='user.user'),
        ),
        migrations.CreateModel(
            name='CourtStaff',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='user.courtbranch')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='court_staff', to='user.user')),
            ],
        ),
        migrations.AddField(
            model_name='courtmanager',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='court_manager', to='user.user'),
        ),
    ]
