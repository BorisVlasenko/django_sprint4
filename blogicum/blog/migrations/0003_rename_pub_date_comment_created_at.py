# Generated by Django 3.2.16 on 2024-05-06 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20240506_2044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='pub_date',
            new_name='created_at',
        ),
    ]
