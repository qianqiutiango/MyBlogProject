# Generated by Django 2.2.3 on 2019-11-12 14:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20191106_1417'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_time'], 'verbose_name': '文章', 'verbose_name_plural': '文章'},
        ),
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 12, 14, 36, 17, 116549, tzinfo=utc), verbose_name='创建时间'),
        ),
    ]
