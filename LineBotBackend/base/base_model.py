from django.db.models import AutoField, DateTimeField
from safedelete.models import SafeDeleteModel


class BaseModel(SafeDeleteModel):
    id = AutoField(primary_key=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True
