# Generated by Django 4.1.5 on 2023-02-03 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('운동', '운동'), ('여행', '여행'), ('문화관람', '문화관람'), ('게임', '게임'), ('음악', '음악'), ('사교/인맥', '사교/인맥'), ('봉사', '봉사'), ('자유주제', '자유주제')], default='자유주제', max_length=20),
        ),
    ]