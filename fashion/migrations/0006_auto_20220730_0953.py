# Generated by Django 3.2.12 on 2022-07-30 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0005_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='description',
            new_name='desc',
        ),
        migrations.AddField(
            model_name='product',
            name='long_desc',
            field=models.TextField(default=''),
        ),
    ]