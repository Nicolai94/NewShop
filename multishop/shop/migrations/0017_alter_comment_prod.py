# Generated by Django 4.1 on 2022-08-20 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_alter_comment_prod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='shop.product'),
        ),
    ]