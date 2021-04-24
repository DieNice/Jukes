# Generated by Django 3.2 on 2021-04-23 06:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('juke', '0006_follower'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follower',
            name='follower_name',
        ),
        migrations.RemoveField(
            model_name='follower',
            name='user_name',
        ),
        migrations.AddField(
            model_name='follower',
            name='follower',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='follower',
            name='follows',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]