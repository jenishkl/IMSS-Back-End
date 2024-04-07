# Generated by Django 4.2.4 on 2024-03-11 17:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import newapp.model_s.productModels
import newapp.model_s.shopCategoryModel
import newapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_shop', models.BooleanField(default=False)),
                ('is_customer', models.BooleanField(default=False)),
                ('shopName', models.CharField(default='', max_length=50, null=True, unique=True)),
                ('unique_shopName', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('company_logo', models.ImageField(blank=True, null=True, upload_to=newapp.models.get_upload_path)),
                ('background_image', models.ImageField(blank=True, null=True, upload_to=newapp.models.banner_upload_path)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('long', models.FloatField(blank=True, null=True)),
                ('about', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_number', models.IntegerField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Kart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'kart',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('unique_name', models.CharField(max_length=50, unique=True)),
                ('parent', models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, to='newapp.location')),
            ],
            options={
                'db_table': 'location',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MainCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('unique_name', models.CharField(max_length=50, unique=True)),
                ('parent', models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='newapp.maincategory')),
            ],
            options={
                'db_table': 'maincategory',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MyCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('unique_name', models.CharField(max_length=50, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=newapp.model_s.shopCategoryModel.get_upload_path)),
                ('parent', models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='newapp.mycategory')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_category', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'myCategory',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('unique_name', models.CharField(default='', max_length=50)),
                ('description', models.CharField(default='', max_length=550)),
                ('original_price', models.FloatField()),
                ('selling_price', models.FloatField()),
                ('stock', models.FloatField()),
                ('is_have_size', models.BooleanField(default=False)),
                ('is_deliverable', models.BooleanField(default=False)),
                ('deliverable_range', models.FloatField(blank=True, null=True)),
                ('delivery_charge_per_km', models.FloatField(blank=True, null=True)),
                ('measurement', models.CharField(blank=True, choices=[('KG', 'Kilograms'), ('L', 'Litre'), ('M', 'Meter'), ('KM', 'KiloMeter'), ('IN', 'Inch'), ('CM', 'CentiMeter'), ('F', 'Feet'), ('T', 'Ton'), ('Y', 'Yard'), ('CS', 'CustomSizes')], max_length=100, null=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('main_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='newapp.maincategory')),
                ('my_category', models.ManyToManyField(to='newapp.mycategory')),
                ('shop_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shop_name', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'products',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=newapp.model_s.productModels.get_upload_path)),
                ('aspect_ratio', models.FloatField(blank=True, null=True)),
                ('primary', models.BooleanField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='newapp.products')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
                ('phone_number', models.CharField(blank=True, default=0, max_length=15)),
                ('lat', models.FloatField(default=0)),
                ('lon', models.FloatField(default=0)),
                ('total_cost', models.FloatField(default=0)),
                ('total_discount', models.FloatField(default=0)),
                ('delivery_cost', models.FloatField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('kart_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kart_id', to='newapp.kart')),
                ('location_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_id', to='newapp.location')),
            ],
            options={
                'db_table': 'orders',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='kart',
            name='product',
            field=models.ManyToManyField(to='newapp.products'),
        ),
        migrations.AddField(
            model_name='kart',
            name='shop_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shop_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='kart',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=200, upload_to='ctimg')),
                ('primary', models.BooleanField(blank=True, default=False)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_images', to='newapp.maincategory')),
            ],
            options={
                'db_table': 'main_category_image',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='customuser',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='newapp.location'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='main_category',
            field=models.ManyToManyField(to='newapp.maincategory'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
