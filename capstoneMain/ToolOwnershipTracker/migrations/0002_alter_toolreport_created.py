# Generated by Django 4.1.2 on 2023-04-18 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToolOwnershipTracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolreport',
            name='created',
            field=models.DateField(),
        ),
    ]