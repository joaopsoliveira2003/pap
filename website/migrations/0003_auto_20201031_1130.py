# Generated by Django 3.1.1 on 2020-10-31 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20201031_1111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactmodel',
            old_name='assunto',
            new_name='message',
        ),
        migrations.RenameField(
            model_name='contactmodel',
            old_name='mensagem',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='contactmodel',
            old_name='nome',
            new_name='subject',
        ),
    ]
