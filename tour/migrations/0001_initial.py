# Generated by Django 3.2.9 on 2021-11-05 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, max_length=200, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PackageTour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tour_name', models.CharField(max_length=50)),
                ('tour_content', models.TextField()),
                ('tour_image', models.ImageField(upload_to='tour/images/%Y/%m/%d')),
                ('tour_price', models.CharField(max_length=10)),
                ('head_image', models.ImageField(blank=True, upload_to='tour/images/%Y/%m/%d')),
                ('head_text', models.CharField(blank=True, max_length=100)),
                ('tour_start_day', models.DateTimeField()),
                ('tour_end_day', models.DateTimeField()),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tour.category')),
                ('tags', models.ManyToManyField(blank=True, to='tour.Tag')),
            ],
        ),
    ]
