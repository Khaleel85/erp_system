# Generated by Django 4.1.5 on 2023-07-18 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_leave'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='reason',
            field=models.TextField(blank=True, help_text='add additional information for leave', max_length=255, null=True, verbose_name='Reason for Leave'),
        ),
        migrations.AlterField(
            model_name='leave',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Canceled', 'Canceled')], default='pending', max_length=12),
        ),
    ]
