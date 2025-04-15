from django.db import models

class UseCase(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('deployed', 'Deployed'),
    ]

    name = models.CharField(max_length=255, unique=True)
    confluence_link = models.URLField(verbose_name="Confluence Page URL")
    splunk_link = models.URLField(verbose_name="Splunk Dashboard URL")
    grafana_link = models.URLField(verbose_name="Grafana Dashboard URL")
    error_list_link = models.URLField(verbose_name="Error List URL")
    gameplan = models.FileField(upload_to='usecases/gameplans/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HubCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class HubLink(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    category = models.ForeignKey(HubCategory, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.contrib.auth.models import User

class HubUserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.ForeignKey(HubLink, on_delete=models.CASCADE)
    last_accessed = models.DateTimeField(auto_now=True)
    access_count = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'link')


class ServerHost(models.Model):
    name = models.CharField(max_length=100, help_text="Label for this server (e.g., Production Jumpbox)")
    jumpbox_ip_or_hostname = models.CharField(max_length=255, help_text="Can be IP or DNS name")
    username = models.CharField(max_length=100, help_text="User to connect into jumpbox")
    
    auth_type = models.CharField(
        choices=[('pem', 'PEM File'), ('password', 'Password')],
        max_length=20
    )
    pem_file = models.FileField(upload_to='keys/', blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.jumpbox_ip_or_hostname})"
