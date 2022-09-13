# Generated by Django 3.2.14 on 2022-09-13 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0112_auto_20220909_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='su_from',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='su_to', to='assets.account', verbose_name='Su from'),
        ),
        migrations.AddField(
            model_name='historicalaccount',
            name='su_from',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='assets.account', verbose_name='Su from'),
        ),
    ]
