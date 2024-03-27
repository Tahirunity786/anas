from django.db import models

# Create your models here.

class Enginetempstorage(models.Model):
    Image = models.ImageField(upload_to="temp/dicom", db_index=True)
    date_created = models.DateTimeField(auto_now_add=True)