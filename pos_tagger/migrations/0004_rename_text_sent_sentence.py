# Generated by Django 5.1.2 on 2024-12-04 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pos_tagger', '0003_rename_sentence_sent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sent',
            old_name='text',
            new_name='sentence',
        ),
    ]
