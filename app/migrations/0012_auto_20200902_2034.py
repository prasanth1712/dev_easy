# Generated by Django 3.0.3 on 2020-09-02 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_lookups_lookup_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lookups',
            options={'ordering': ['lookup_order']},
        ),
        migrations.AddField(
            model_name='wmobject',
            name='app_imp',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='wmobject',
            name='objective',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='wmobject',
            name='proc_imp',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='wmobject',
            name='resolution',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]