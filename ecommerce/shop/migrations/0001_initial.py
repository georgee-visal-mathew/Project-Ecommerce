# Generated by Django 5.0.7 on 2024-07-16 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('desc', models.TextField(default='')),
                ('offprice', models.CharField(max_length=20)),
            ],
        ),
    ]