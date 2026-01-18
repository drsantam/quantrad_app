from django.db import models

# Create your models here.

class LookupAbstract(models.Model):
    id = models.CharField(max_length=255,primary_key=True,help_text="Enter the Unique ID or Code")
    label = models.CharField(max_length=1024,help_text="Enter the Label for the Code")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class LookupCancerSite(LookupAbstract):
    
    class Meta:
        verbose_name = "Lookup Cancer Site"
        verbose_name_plural = "Lookup Cancer Sites"


class LookupPathology(LookupAbstract):

    class Meta: 
        verbose_name = "Lookup Pathology"
        verbose_name_plural = "Lookup Pathologies"


class LookupRadiotherapyTreatmentTechnique(LookupAbstract):

    
    class Meta:
        verbose_name = "Lookup Radiotherapy Treatment Techniques"
        verbose_name_plural = "Lookup Radiotherapy Treatment Techniques"


class LookupBillingCode(LookupAbstract):
    
    class Meta:
        verbose_name = "Lookup Billing Code"
        verbose_name_plural = "Lookup Billing Codes"


class LookupSystemicTherapyType(LookupAbstract):
    
    class Meta:
        verbose_name = "Lookup Systemic Therapy Type"
        verbose_name_plural = "Lookup Systemic Therapy Types"