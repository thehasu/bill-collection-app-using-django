# Generated by Django 4.2.1 on 2023-05-14 05:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bill_coll', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='date',
        ),
        migrations.AlterField(
            model_name='collection',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
