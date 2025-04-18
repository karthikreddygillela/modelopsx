# Generated by Django 5.2 on 2025-04-14 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UseCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('confluence_link', models.URLField(verbose_name='Confluence Page URL')),
                ('splunk_link', models.URLField(verbose_name='Splunk Dashboard URL')),
                ('grafana_link', models.URLField(verbose_name='Grafana Dashboard URL')),
                ('error_list_link', models.URLField(verbose_name='Error List URL')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
