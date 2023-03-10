# Generated by Django 4.1.5 on 2023-01-25 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='comment_cnt',
            field=models.SmallIntegerField(default=0, verbose_name='댓글 수'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='participations_cnt',
            field=models.SmallIntegerField(default=0, verbose_name='참여횟수'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='post_cnt',
            field=models.SmallIntegerField(default=0, verbose_name='게시글 수'),
        ),
    ]
