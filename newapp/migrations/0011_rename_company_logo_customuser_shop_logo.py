# Generated by Django 4.2.4 on 2024-03-29 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0010_maincategory_index'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='company_logo',
            new_name='shop_logo',
        ),
    ]
