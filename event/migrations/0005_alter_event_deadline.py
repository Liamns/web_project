# Generated by Django 4.1.5 on 2023-02-06 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_alter_event_event_imgage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='deadline',
            field=models.DateField(verbose_name='마감날짜'),
        ),
    ]