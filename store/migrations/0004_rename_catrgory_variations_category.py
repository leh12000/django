# Generated by Django 5.0.6 on 2024-07-18 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_variations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variations',
            old_name='catrgory',
            new_name='category',
        ),
    ]
