# Generated by Django 5.0.6 on 2024-05-23 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('empid', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('empfname', models.CharField(max_length=64)),
                ('emplname', models.CharField(max_length=64)),
                ('emppasswd', models.CharField(max_length=256)),
                ('emprole', models.IntegerField()),
            ],
        ),
    ]
