# Generated by Django 4.1.4 on 2023-06-10 17:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_coll', '0009_profile_paidthrumonth'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='billDate',
            field=models.DateField(blank=True, default=datetime.datetime.now),
        ),
    ]