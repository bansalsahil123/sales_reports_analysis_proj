# Generated by Django 2.2.8 on 2021-04-20 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='m5.jpg', upload_to='products'),
        ),
    ]