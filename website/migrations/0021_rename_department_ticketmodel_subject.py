# Generated by Django 3.2.3 on 2021-06-23 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0020_auto_20210608_1734'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticketmodel',
            old_name='department',
            new_name='subject',
        ),
    ]
