from django.db import models
from django_jalali.db import models as jmodels


class BaseModel(models.Model):
    created_at = jmodels.jDateTimeField(auto_now_add=True, null=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
