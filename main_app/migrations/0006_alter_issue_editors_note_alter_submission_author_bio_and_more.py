# Generated by Django 5.2.1 on 2025-06-07 23:18

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_rename_issue_status_issue_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='editors_note',
            field=django_ckeditor_5.fields.CKEditor5Field(),
        ),
        migrations.AlterField(
            model_name='submission',
            name='author_bio',
            field=django_ckeditor_5.fields.CKEditor5Field(),
        ),
        migrations.AlterField(
            model_name='submission',
            name='submission_text',
            field=django_ckeditor_5.fields.CKEditor5Field(),
        ),
    ]
