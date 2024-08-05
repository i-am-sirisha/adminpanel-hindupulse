

from django.db import models
import uuid
from .category import Category
from .news_subcategory import NewsSubCategory

class ProductionApNewsModel(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    headline = models.CharField(max_length=255, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=5000, null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    url = models.URLField(max_length=5000, null=True, blank=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, max_length=45,db_column='category_id')
    news_sub_category_id = models.ForeignKey(NewsSubCategory,null=True, on_delete=models.CASCADE,db_column='news_sub_category_id')

    class Meta:
        managed = True
        db_table = "production_ap_news"
    
    def __str__(self):
        return self.headline
