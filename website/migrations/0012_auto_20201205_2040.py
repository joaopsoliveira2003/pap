# Generated by Django 3.1.4 on 2020-12-05 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_filemodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='filemodel',
            options={'ordering': ['id'], 'verbose_name': 'Ficheiro', 'verbose_name_plural': 'Ficheiros'},
        ),
    ]
