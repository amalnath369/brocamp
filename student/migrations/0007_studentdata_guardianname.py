# Generated by Django 5.0.6 on 2025-01-07 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_alter_employeedata_designation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentdata',
            name='guardianname',
            field=models.CharField(default='test', max_length=100),
        ),
    ]