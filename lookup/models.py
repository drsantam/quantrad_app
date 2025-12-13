from django.db import models

# Create your models here.

class LookupAbstract(models.Model):
    id = models.CharField(max_length=255,primary_key=True,help_text="Enter the Unique ID or Code")
    name = models.CharField(max_length=1024,help_text="Enter the Name")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class LookupDiagnosis(LookupAbstract):

    class Meta: 
        verbose_name = "Lookup Diagnosis"
        verbose_name_plural = "Lookup Diagnoses"
      