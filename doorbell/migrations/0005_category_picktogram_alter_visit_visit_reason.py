# Generated by Django 4.1 on 2022-09-03 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doorbell', '0004_alter_visit_visit_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='picktogram',
            field=models.ImageField(null=True, upload_to='pictogram/image', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='visit',
            name='visit_reason',
            field=models.TextField(blank=True, verbose_name='Visit Reason'),
        ),
    ]
