# Generated by Django 3.2.6 on 2022-08-09 11:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0011_auto_20220808_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='catagory',
            name='slug',
            field=models.CharField(default=django.utils.timezone.now, max_length=150),
            preserve_default=False,
        ),
    ]
