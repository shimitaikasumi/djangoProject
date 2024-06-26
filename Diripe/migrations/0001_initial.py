# Generated by Django 5.0.6 on 2024-06-25 05:16

import django.db.models.deletion
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
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('medicineid', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('medicinename', models.CharField(max_length=64)),
                ('unit', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('patid', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('patfname', models.CharField(max_length=64)),
                ('patlname', models.CharField(max_length=64)),
                ('hokenmei', models.CharField(max_length=64)),
                ('hokenexp', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Shiiregyosya',
            fields=[
                ('shiireid', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('shiiremei', models.CharField(max_length=64)),
                ('shiireaddress', models.CharField(max_length=64)),
                ('shiiretel', models.CharField(max_length=13)),
                ('shihonkin', models.IntegerField()),
                ('nouki', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('treatment_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('empid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Diripe.employee')),
                ('medicineid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Diripe.medicine')),
                ('patid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Diripe.patient')),
            ],
        ),
    ]
