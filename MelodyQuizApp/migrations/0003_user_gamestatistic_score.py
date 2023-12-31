# Generated by Django 4.2.4 on 2023-08-16 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MelodyQuizApp', '0002_answer_gamestatistic_question_userprogress_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leaderboard', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='gamestatistic',
            name='score',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
