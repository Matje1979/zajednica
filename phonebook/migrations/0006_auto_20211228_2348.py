# Generated by Django 2.2.7 on 2021-12-28 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0005_phonecategory_numbers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonecategory',
            name='numbers',
            field=models.CharField(blank=True, default='', max_length=80),
        ),
    ]
