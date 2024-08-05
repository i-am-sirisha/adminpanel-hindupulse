
import uuid
from django.db import models

class Category(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    name = models.CharField(db_column='name', max_length=100, unique=True)
    priority_order = models.IntegerField(default=0)
    
    class Meta:
        managed = True
        db_table = "category"
    
    def __str__(self):
        return f'{self.name}'
