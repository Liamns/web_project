# Generated by Django 4.1.5 on 2023-02-06 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0005_alter_event_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL, verbose_name='작성자'),
        ),
    ]
