# Generated by Django 5.0.4 on 2024-05-09 20:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("applicants", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="application",
            old_name="student",
            new_name="applicant",
        ),
    ]
