# Generated by Django 2.1.15 on 2020-01-05 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200105_0843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.TextField(blank=True, max_length=1024, null=True, verbose_name='City'),
        ),
    ]