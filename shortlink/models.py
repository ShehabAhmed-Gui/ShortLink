from django.db import models

class Urls(models.Model):
    long_url = models.CharField(max_length=200, null=False)
    short_url = models.CharField(max_length=20, unique=True, null=False)
    created_at = models.DateTimeField()
    # If a link isn't clicked in one month, it 'll be deactivated
    deactivate_date = models.DateTimeField()