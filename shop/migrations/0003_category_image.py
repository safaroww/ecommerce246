# Generated by Django 5.0.1 on 2024-01-24 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_remove_category_products_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='asd', upload_to='categories'),
            preserve_default=False,
        ),
    ]
