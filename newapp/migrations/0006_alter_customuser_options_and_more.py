# Generated by Django 4.2.4 on 2024-03-17 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0005_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='customuser',
            unique_together={('email',)},
        ),
    ]
