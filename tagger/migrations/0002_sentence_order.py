# Generated by Django 5.1.2 on 2024-12-07 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tagger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentence',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
