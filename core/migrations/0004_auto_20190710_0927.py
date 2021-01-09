# Generated by Django 2.2.3 on 2019-07-10 09:27

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.CharField(default=core.models.pkgen, max_length=8, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(editable=False, max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together={('author', 'id')},
        ),
    ]
