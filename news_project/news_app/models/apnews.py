
        
from django.db import models
import uuid
from .category import Category
from .news_subcategory import NewsSubCategory

class StagingApNewsModel(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid4, unique=True, editable=False)
    headline = models.CharField(max_length=255, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=5000, null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    url = models.URLField(max_length=5000, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(NewsSubCategory, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        managed = True
        db_table = "ap_news"
    
    def __str__(self):
        return self.headline
