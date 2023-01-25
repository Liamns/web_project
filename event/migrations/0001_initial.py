# Generated by Django 4.1.5 on 2023-01-25 02:32

from django.db import migrations, models
import django.db.models.deletion
import event.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='등록일자')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='수정일자')),
                ('location_tags', models.CharField(max_length=128, verbose_name='지역태그')),
                ('content', models.TextField(default='', verbose_name='내용')),
                ('title', models.CharField(max_length=256, verbose_name='제목')),
                ('deadline', models.DateTimeField(verbose_name='마감날짜')),
                ('participants_limit', models.SmallIntegerField(verbose_name='참여인원 제한 수')),
                ('start_event', models.CharField(max_length=50, verbose_name='이벤트 시작일')),
                ('end_event', models.CharField(max_length=50, verbose_name='이벤트 종료일')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='EventImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_img', models.ImageField(upload_to=event.models.image_upload_to)),
            ],
        ),
        migrations.CreateModel(
            name='Participants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.event')),
            ],
        ),
    ]
