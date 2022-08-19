# Generated by Django 4.1 on 2022-08-17 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_reviews'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reviews',
            options={'verbose_name': 'Review', 'verbose_name_plural': 'Reviews'},
        ),
        migrations.AlterField(
            model_name='reviews',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.reviews', verbose_name='Parent'),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='text',
            field=models.TextField(max_length=2000, verbose_name='Description'),
        ),
    ]