# Generated by Django 5.1.3 on 2024-11-16 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_usermodel_last_login'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leavemodel',
            old_name='leave_granted',
            new_name='leave_status',
        ),
    ]