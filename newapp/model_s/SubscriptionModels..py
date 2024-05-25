
from django.db import models
from newapp.models import CustomUser

class Subscriptions(models.Model):
    title = models.TextField(
        null=False, blank=True, default=0)
    description = models.TextField(
        null=False, blank=True, default=0)
    user = models.ForeignKey(
        CustomUser, unique=False, null=True, on_delete=models.SET_NULL,)
    seen = models.BooleanField(default=False)
    source= models.TextField(
        null=False, blank=True, default=0)
    class Meta:
        managed = True
        db_table = "notifications"
