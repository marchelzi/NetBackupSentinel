# Generated by Django 4.2.1 on 2023-05-20 09:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ndam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='devicebackup',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='devicecredential',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
