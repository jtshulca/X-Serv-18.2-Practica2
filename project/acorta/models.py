from django.db import models

# Create your models here.
class Urls(models.Model):
	URL_larga = models.CharField(max_length=32)
