# Generated by Django 3.2.3 on 2021-06-08 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0018_auto_20210603_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketmodel',
            name='email',
        ),
        migrations.RemoveField(
            model_name='ticketmodel',
            name='name',
        ),
    ]