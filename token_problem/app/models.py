import uuid
from django.db import models

# Create your models here.


class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.CharField(max_length=320)
    created_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(default=None, null=True, blank=True)
    last_used = models.DateTimeField(default=None, null=True, blank=True)
    is_assigned = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
