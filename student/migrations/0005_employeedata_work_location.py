# Generated by Django 5.0.6 on 2024-12-28 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_employeedata_designation'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeedata',
            name='Work_location',
            field=models.CharField(default='test', max_length=50),
        ),
    ]
