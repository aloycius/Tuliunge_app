# Generated by Django 5.1.2 on 2024-10-31 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('license_number', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]
