from django.db import models
import uuid

class ApNewsModel(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    headline = models.CharField(max_length=255)
    summary = models.TextField()
    link = models.URLField()
    image=models.TextField()

    url = models.URLField()

    def __str__(self):
        return self.headline
    class Meta:
        managed = False
        db_table = "ap_news"
        
        