# Generated by Django 4.1.5 on 2023-02-03 08:20

from django.db import migrations, models
import event.models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_alter_event_event_imgage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_imgage',
            field=models.ImageField(default='default/default.png', upload_to=event.models.image_upload_to),
        ),
    ]
