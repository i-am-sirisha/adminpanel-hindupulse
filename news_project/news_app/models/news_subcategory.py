
import uuid
from django.db import models
from .category import Category

class NewsSubCategory(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    name = models.CharField(db_column='name', max_length=100)
    other_category = models.ForeignKey(Category, db_column='category_id1', max_length=45, on_delete=models.CASCADE, related_name='subcategories')
    
    class Meta:
        managed = True
        db_table = "sub_category"
    
    def __str__(self):
        return f'{self.name}'
