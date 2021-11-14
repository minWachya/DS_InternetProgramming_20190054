# Generated by Django 3.2.9 on 2021-11-13 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0003_auto_20211110_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='TourAgency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=300)),
                ('contact_number', models.CharField(max_length=20)),
                ('logo', models.ImageField(upload_to='agency/images/%Y/%m/%d')),
            ],
        ),
        migrations.AddField(
            model_name='packagetour',
            name='agency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tour.touragency'),
        ),
    ]