# Generated by Django 2.0.1 on 2018-01-09 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0003_remove_profile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cats.Profile'),
        ),
    ]