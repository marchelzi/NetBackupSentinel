# Generated by Django 4.2.1 on 2023-05-20 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ndam', '0002_alter_device_id_alter_devicebackup_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='enabled',
            field=models.BooleanField(default=True, help_text='Enable or disable device backup'),
        ),
    ]