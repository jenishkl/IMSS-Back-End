# Generated by Django 4.2.4 on 2024-03-17 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0002_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='shopName',
            field=models.CharField(blank=True, error_messages={'unique': 'unique.'}, max_length=50, null=True, unique=True),
        ),
    ]
