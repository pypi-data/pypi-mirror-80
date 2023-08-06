import datetime
import uuid

from django.db import models


class AuditoryModel(models.Model):
    __abstract__ = True

    created_by = models.UUIDField(required=True, default=uuid.uuid4)
    created_date = models.DateTimeField(required=True, default=datetime.datetime.now)
    updated_by = models.UUIDField(required=True, default=uuid.uuid4)
    updated_date = models.DateTimeField(required=True, default=datetime.datetime.now)
