# Generated by Django 4.2.4 on 2023-12-09 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0018_alter_customuser_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='unique_shopName',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]