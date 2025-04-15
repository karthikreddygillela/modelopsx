# Generated by Django 5.2 on 2025-04-15 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_usecase_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='serverhost',
            old_name='jumpbox_auth_type',
            new_name='auth_type',
        ),
        migrations.RenameField(
            model_name='serverhost',
            old_name='jumpbox_password',
            new_name='password',
        ),
        migrations.RenameField(
            model_name='serverhost',
            old_name='jumpbox_pem_file',
            new_name='pem_file',
        ),
        migrations.RemoveField(
            model_name='serverhost',
            name='jumpbox_ip',
        ),
        migrations.RemoveField(
            model_name='serverhost',
            name='jumpbox_username',
        ),
        migrations.RemoveField(
            model_name='serverhost',
            name='target_auth_type',
        ),
        migrations.RemoveField(
            model_name='serverhost',
            name='target_ip',
        ),
        migrations.RemoveField(
            model_name='serverhost',
            name='target_password',
        ),
        migrations.RemoveField(
            model_name='serverhost',
            name='target_pem_file',
        ),
        migrations.RemoveField(
            model_name='serverhost',
            name='target_username',
        ),
        migrations.AddField(
            model_name='serverhost',
            name='jumpbox_ip_or_hostname',
            field=models.CharField(default='127.0.0.1', help_text='Can be IP or DNS name', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='serverhost',
            name='username',
            field=models.CharField(default='karthik', help_text='User to connect into jumpbox', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='serverhost',
            name='name',
            field=models.CharField(help_text='Label for this server (e.g., Production Jumpbox)', max_length=100),
        ),
    ]
