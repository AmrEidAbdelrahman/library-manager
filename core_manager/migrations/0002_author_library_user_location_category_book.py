# Generated by Django 5.0.2 on 2025-06-07 11:12

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('biography', models.TextField(blank=True, verbose_name='biography')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='birth date')),
                ('death_date', models.DateField(blank=True, null=True, verbose_name='death date')),
                ('nationality', models.CharField(blank=True, max_length=100, verbose_name='nationality')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'author',
                'verbose_name_plural': 'authors',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('address', models.TextField(verbose_name='address')),
                ('phone', models.CharField(max_length=15, verbose_name='phone')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('website', models.URLField(blank=True, verbose_name='website')),
                ('location', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326, verbose_name='location')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'library',
                'verbose_name_plural': 'libraries',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326, verbose_name='location'),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core_manager.category')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('isbn', models.CharField(max_length=13, unique=True, verbose_name='ISBN')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('publication_date', models.DateField(blank=True, null=True, verbose_name='publication date')),
                ('publisher', models.CharField(blank=True, max_length=255, verbose_name='publisher')),
                ('language', models.CharField(blank=True, max_length=50, verbose_name='language')),
                ('pages', models.PositiveIntegerField(blank=True, null=True, verbose_name='pages')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='book_covers/', verbose_name='cover image')),
                ('total_copies', models.PositiveIntegerField(default=1, verbose_name='total copies')),
                ('available_copies', models.PositiveIntegerField(default=1, verbose_name='available copies')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='core_manager.author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='core_manager.category')),
                ('library', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='core_manager.library')),
            ],
            options={
                'verbose_name': 'book',
                'verbose_name_plural': 'books',
                'ordering': ['title'],
                'indexes': [models.Index(fields=['title'], name='core_manage_title_7228c1_idx'), models.Index(fields=['isbn'], name='core_manage_isbn_7a6ca6_idx')],
            },
        ),
    ]
