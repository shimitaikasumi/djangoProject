# Generated by Django 5.0.6 on 2024-06-14 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Diripe', '0003_patient'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('medicineid', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('medicinename', models.CharField(max_length=64)),
                ('unit', models.CharField(max_length=8)),
            ],
        ),
    ]