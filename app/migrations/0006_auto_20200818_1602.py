# Generated by Django 3.0.3 on 2020-08-18 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_lookups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wmobject_details',
            name='object_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.lookups'),
        ),
    ]