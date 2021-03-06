# Generated by Django 3.1.2 on 2021-05-24 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_auto_20210524_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.registration'),
        ),
        migrations.AlterField(
            model_name='onlineoffline',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.registration'),
        ),
        migrations.AlterField(
            model_name='personal',
            name='me',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.registration'),
        ),
    ]
