# Generated by Django 3.2.3 on 2021-06-03 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0017_alter_profile_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contactuser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contactmodel',
            name='technician',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contacttechnician', to=settings.AUTH_USER_MODEL),
        ),
    ]
