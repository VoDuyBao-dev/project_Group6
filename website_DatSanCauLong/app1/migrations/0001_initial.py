# Generated by Django 5.1.4 on 2025-02-12 10:34

import app1.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BadmintonHall',
            fields=[
                ('badminton_hall_id', models.CharField(default=app1.models.generate_short_id, editable=False, max_length=5, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PaymentAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accountHolder', models.CharField(max_length=50)),
                ('accountNumber', models.CharField(max_length=20)),
                ('paymentMethod', models.CharField(choices=[('bank', 'Ngân hàng'), ('momo', 'Momo')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlotTemplate',
            fields=[
                ('template_id', models.CharField(default=app1.models.generate_short_id, editable=False, max_length=5, primary_key=True, serialize=False)),
                ('day_of_week', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=20)),
                ('time_frame', models.CharField(max_length=50)),
                ('fixed_price', models.DecimalField(decimal_places=3, max_digits=6)),
                ('daily_price', models.DecimalField(decimal_places=3, max_digits=6)),
                ('flexible_price', models.DecimalField(decimal_places=3, max_digits=6)),
                ('status', models.CharField(choices=[('available', 'Available'), ('unavailable', 'Unavailable')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Court',
            fields=[
                ('court_id', models.CharField(default=app1.models.generate_short_id, editable=False, max_length=5, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('status', models.CharField(choices=[('under_maintenance', 'Under Maintenance'), ('empty', 'Empty'), ('booked', 'Booked')], default='empty', max_length=20)),
                ('badminton_hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courts', to='app1.badmintonhall')),
            ],
        ),
        migrations.CreateModel(
            name='CourtStaff',
            fields=[
                ('court_staff_id', models.CharField(default=app1.models.generate_short_id, editable=False, max_length=5, primary_key=True, serialize=False)),
                ('court', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='court_staff', to='app1.court')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='court_staff', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.CharField(default=app1.models.generate_short_id, editable=False, max_length=5, primary_key=True, serialize=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.CharField(default=app1.models.generate_short_id, editable=False, max_length=5, primary_key=True, serialize=False)),
                ('booking_type', models.CharField(choices=[('fixed', 'Fixed'), ('daily', 'Daily'), ('flexible', 'Flexible')], max_length=20)),
                ('date', models.DateField()),
                ('start_time', models.TimeField(default='00:00:00')),
                ('end_time', models.TimeField(default='00:00:00')),
                ('status', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('court_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='app1.court')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='app1.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.CharField(default=app1.models.generate_short_id, editable=False, max_length=5, primary_key=True, serialize=False)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('booking_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='app1.booking')),
                ('customer_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='app1.customer')),
                ('payment_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='app1.paymentaccount')),
            ],
        ),
        migrations.CreateModel(
            name='CourtManager',
            fields=[
                ('courtManager_id', models.CharField(default=app1.models.generate_short_id, editable=False, max_length=5, primary_key=True, serialize=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='court_manager', to=settings.AUTH_USER_MODEL)),
                ('payment_account', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='court_manager', to='app1.paymentaccount')),
            ],
        ),
        migrations.CreateModel(
            name='RevenueReport',
            fields=[
                ('revenueReport_id', models.CharField(default=app1.models.generate_short_id, editable=False, max_length=5, primary_key=True, serialize=False)),
                ('total_revenue', models.DecimalField(decimal_places=2, max_digits=15)),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
                ('badminton_hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revenue_reports', to='app1.badmintonhall')),
                ('payments', models.ManyToManyField(related_name='revenues', to='app1.payment')),
            ],
        ),
        migrations.CreateModel(
            name='SystemAdmin',
            fields=[
                ('systemAdmin_id', models.CharField(default=app1.models.generate_short_id, editable=False, max_length=5, primary_key=True, serialize=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='system_admin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
