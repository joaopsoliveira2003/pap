# Generated by Django 3.1.4 on 2020-12-05 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='github',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='profile',
            name='twitter',
            field=models.TextField(null=True),
        ),
    ]
