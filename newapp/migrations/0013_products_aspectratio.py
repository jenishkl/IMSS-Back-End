# Generated by Django 4.2.4 on 2024-03-31 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0012_alter_mycategory_name_alter_mycategory_unique_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='aspectRatio',
            field=models.FloatField(default=1),
        ),
    ]
