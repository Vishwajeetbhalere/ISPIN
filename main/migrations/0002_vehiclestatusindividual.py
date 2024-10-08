# Generated by Django 5.1.1 on 2024-09-05 14:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleStatusIndividual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_latitude', models.DecimalField(decimal_places=6, default=0.0, max_digits=9)),
                ('current_longitude', models.DecimalField(decimal_places=6, default=0.0, max_digits=9)),
                ('starting_latitude', models.DecimalField(decimal_places=6, default=0.0, max_digits=9)),
                ('starting_longitude', models.DecimalField(decimal_places=6, default=0.0, max_digits=9)),
                ('ending_latitude', models.DecimalField(blank=True, decimal_places=6, default=0.0, max_digits=9, null=True)),
                ('ending_longitude', models.DecimalField(blank=True, decimal_places=6, default=0.0, max_digits=9, null=True)),
                ('panic_button_status', models.BooleanField(default=False)),
                ('main_battery_temp', models.CharField(max_length=50)),
                ('main_battery_current', models.DecimalField(decimal_places=2, max_digits=5)),
                ('auxiliary_battery_status', models.DecimalField(decimal_places=2, max_digits=5)),
                ('lock_status', models.BooleanField(default=False)),
                ('route', models.TextField()),
                ('emergency_owner_whatsapp', models.CharField(max_length=255)),
                ('geo_fencing_distance', models.CharField(blank=True, max_length=20, null=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_status', to='main.individualowner')),
            ],
        ),
    ]
