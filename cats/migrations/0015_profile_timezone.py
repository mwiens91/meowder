# Generated by Django 2.0.1 on 2018-02-07 00:47

from django.db import migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0014_auto_20180206_0359'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(default='Canada/Pacific'),
        ),
    ]