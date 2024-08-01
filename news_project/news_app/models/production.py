from django.db import models
import uuid

class ProductionApNewsModel(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    headline = models.CharField(max_length=255,null=True,blank=True)
    summary = models.TextField(null=True,blank=True)
    link = models.URLField(null=True,blank=True)
    image = models.TextField(null=True,blank=True)
    url = models.URLField(null=True,blank=True)

    def __str__(self):
        return self.headline

    class Meta:
        managed = True
        db_table = "production_ap_news"
