# Generated by Django 3.1.2 on 2021-05-20 09:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('room', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='OnlineOffline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('me', models.CharField(max_length=255)),
                ('user', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=255)),
                ('messages', models.TextField()),
                ('datetime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('people', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.personal')),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('datetime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.groups')),
            ],
        ),
    ]
