# Generated by Django 3.0.7 on 2020-06-16 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConsentRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=512)),
                ('confirmed_on', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.BinaryField(max_length=16)),
                ('referrer', models.CharField(max_length=16384)),
                ('user_agent', models.CharField(max_length=16384)),
                ('status_flag', models.BooleanField()),
                ('status', models.BinaryField()),
            ],
        ),
        migrations.CreateModel(
            name='ExpiryLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_run', models.DateTimeField(auto_now_add=True)),
                ('run_reason', models.CharField(max_length=200)),
            ],
        ),
    ]
