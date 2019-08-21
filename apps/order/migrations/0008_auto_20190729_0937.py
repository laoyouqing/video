# Generated by Django 2.1.1 on 2019-07-29 01:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20190729_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='user',
            field=models.ForeignKey(help_text='下单用户', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='下单用户'),
        ),
    ]
