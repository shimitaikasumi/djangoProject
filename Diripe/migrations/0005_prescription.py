# Generated by Django 5.0.6 on 2024-06-18 05:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Diripe', '0004_medicine'),
    ]

    operations = [
        migrations.CreateModel(
            name='prescription',
            fields=[
                ('prescriptionid', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('prescquantity', models.IntegerField()),
                ('date_prescribed', models.DateField(auto_now_add=True)),
                ('prescdays', models.IntegerField()),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Diripe.medicine')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Diripe.patient')),
            ],
        ),
    ]