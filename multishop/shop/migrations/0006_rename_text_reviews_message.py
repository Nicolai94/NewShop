# Generated by Django 4.1 on 2022-08-18 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_reviews_options_alter_reviews_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviews',
            old_name='text',
            new_name='message',
        ),
    ]
