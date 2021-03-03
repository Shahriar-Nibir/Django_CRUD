# Generated by Django 3.1.2 on 2020-11-14 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_order_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='tag',
        ),
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(to='account.Tags'),
        ),
    ]
