# Generated by Django 4.1.4 on 2023-06-05 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bill_coll', '0005_alter_collection_billmonth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='billMonth',
            field=models.ForeignKey(default=6, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bill_coll.month'),
        ),
    ]