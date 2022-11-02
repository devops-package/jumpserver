# Generated by Django 3.2.14 on 2022-11-02 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('terminal', '0056_auto_20221101_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='applethost',
            name='terminal',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='applet_host', to='terminal.terminal', verbose_name='Terminal'),
        ),
        migrations.AlterField(
            model_name='appletpublication',
            name='status',
            field=models.CharField(default='ready', max_length=16, verbose_name='Status'),
        ),
    ]
