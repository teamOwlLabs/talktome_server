# Generated by Django 4.1 on 2022-09-03 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doorbell', '0005_category_picktogram_alter_visit_visit_reason'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='picktogram',
            new_name='pictogram',
        ),
    ]
