# Generated by Django 5.0.3 on 2024-05-15 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clinic', '0009_remove_appointment_day_appointment_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='age',
        ),
        migrations.AddField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(default='2000-1-1'),
        ),
    ]
