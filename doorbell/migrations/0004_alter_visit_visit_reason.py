# Generated by Django 4.1 on 2022-09-01 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doorbell', '0003_category_rgb_color_category_vibration_pattern_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='visit_reason',
            field=models.TextField(blank=True, verbose_name='Visti Reason'),
        ),
    ]
