# Generated by Django 2.0 on 2018-01-01 04:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LAssignTo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Name')),
                ('position', models.CharField(max_length=300, verbose_name='Position')),
                ('desc', models.CharField(max_length=300, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letter_received', models.DateTimeField(verbose_name='Letter Received')),
                ('letter_ref', models.CharField(max_length=300, unique=True, verbose_name='Outside Ref. Number')),
                ('sector_ref', models.CharField(max_length=300, unique=True, verbose_name='Sector Ref. Number')),
                ('letter_date', models.DateTimeField(verbose_name='Letter Date')),
                ('letter_from', models.CharField(max_length=300, verbose_name='Letter From')),
                ('letter_desc', models.TextField(verbose_name='Topics')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Date Key-In')),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letter.LAssignTo')),
            ],
        ),
        migrations.CreateModel(
            name='LHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=300, verbose_name='Name')),
                ('h_date', models.DateTimeField(auto_now_add=True, verbose_name='Date Created/Updated')),
                ('userby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
