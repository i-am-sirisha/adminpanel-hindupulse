# Generated by Django 5.0.7 on 2024-07-31 22:13

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='cnbcNewsModel',
            fields=[
                ('_id', models.CharField(db_column='_id', default=uuid.uuid1, editable=False, max_length=45, primary_key=True, serialize=False, unique=True)),
                ('headline', models.CharField(max_length=255)),
                ('summary', models.TextField()),
                ('link', models.URLField()),
                ('image', models.TextField()),
                ('url', models.URLField()),
            ],
            options={
                'db_table': 'cnbc_news',
                'managed': True,
            },
        ),
        migrations.AlterModelOptions(
            name='apnewsmodel',
            options={'managed': False},
        ),
    ]