# Generated by Django 4.2.4 on 2023-12-02 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0016_alter_customuser_contact_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='contact_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]