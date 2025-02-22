from django.utils import timezone
from mongoengine import Document, DateTimeField


class BaseModel(Document):

    """
    Abstract base model using MongoEngine that includes common fields:
    - created_at: DateTimeField representing the creation timestamp.
    - updated_at: DateTimeField representing the last update timestamp.

    Note: This model is abstract and meant to be inherited by other models.
    """

    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(default=timezone.now)

    meta = {
        'abstract': True,
        'indexes': ['created_at', 'updated_at']
    }

    def save(self, *args, **kwargs):

        # Update the 'updated_at' field on every save.
        self.updated_at = timezone.now()

        # Ensure 'created_at' is set on first save.
        if not self.created_at:
            self.created_at = timezone.now()
        return super().save(*args, **kwargs)

