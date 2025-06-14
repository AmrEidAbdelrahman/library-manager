# Generated by Django 5.0.2 on 2025-06-07 14:46

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0002_author_library_user_location_category_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowed_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='borrowed date')),
                ('due_date', models.DateTimeField(verbose_name='due date')),
                ('returned_date', models.DateTimeField(blank=True, null=True, verbose_name='returned date')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('active', 'Active'), ('returned', 'Returned'), ('overdue', 'Overdue'), ('cancelled', 'Cancelled')], default='pending', max_length=20, verbose_name='status')),
                ('fine_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='fine amount')),
                ('notes', models.TextField(blank=True, verbose_name='notes')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='borrowings', to='core_manager.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='borrowings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'borrowing',
                'verbose_name_plural': 'borrowings',
                'ordering': ['-borrowed_date'],
                'indexes': [models.Index(fields=['status'], name='core_manage_status_acc05d_idx'), models.Index(fields=['due_date'], name='core_manage_due_dat_456e47_idx')],
            },
        ),
    ]
