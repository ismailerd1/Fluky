# Generated by Django 5.0.3 on 2024-04-06 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_message_room_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_seen',
            field=models.BooleanField(default=False),
        ),
    ]
