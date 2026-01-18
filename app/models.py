from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.core.exceptions import ValidationError
from lookup.models import *

# Create your models here.

class GenderChoices(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    OTHER = 'O', 'Other'

class Patient(models.Model):
    '''
    Model to store information about Patient.
    '''
    patient_uid = models.CharField(unique=True,max_length=255,verbose_name = "Patient Hospital Unique ID", help_text="Enter the patient's Hospital Unique ID")
    name = models.CharField(max_length=255,verbose_name = "Patient Name", help_text="Enter the patient's name")
    date_of_birth = models.DateField(verbose_name = "Date of Birth", help_text="Enter the patient's date of birth")
    gender = models.CharField(max_length=10,choices=GenderChoices.choices,verbose_name = "Gender", help_text="Enter the patient's gender")
    date_of_registration = models.DateField(auto_now_add=True,verbose_name = "Date of Registration", help_text="Enter the patient's date of registration")
    age_at_registration = models.GeneratedField(
        expression = models.F('date_of_registration')-models.F('date_of_birth'),
        output_field = models.DurationField(),
        db_persist=True
    )
    created_at = models.DateTimeField(auto_now_add=True,verbose_name = "Created At", help_text="Enter Date Time when this patient's record was created")
    modified_at = models.DateTimeField(auto_now=True,verbose_name = "Modified At", help_text="Enter the Date Time when this patient's record was modified")

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def clean(self):
        super().clean()
        if self.date_of_birth and self.date_of_registration and self.date_of_registration < self.date_of_birth:
            raise ValidationError({
                "date_of_registration": "Date of Registration cannot be earlier than Date of Birth."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.patient_uid})"


class CancerSideChoices(models.TextChoices):
    '''
    Enum to store information about the side of the cancer.
    '''
    LEFT = 'L', 'Left'
    RIGHT = 'R', 'Right'
    BILATERAL = 'BL', 'Bilateral'
    MIDLINE = 'ML', 'Midline'
    CENTRAL = 'C', 'Central'
    NOT_APPLICABLE = 'NA', 'Not Applicable'


class AJCCStagePrefixChoices(models.TextChoices):
    '''
    Enum to store choices related to the prefix for AJCC T, N and M Stage.
    '''
    c = 'c', 'Clinical or radiological'
    p = 'p', 'Pathological'
    r = 'r', 'Retreatment'
    yp = 'yp', 'Post Neoadjuvant Pathological'
    yc = 'yc', 'Post Neoadjuvant Clinical'

class AJCCMajorTStageChoices(models.TextChoices):
    '''
    Enum to store choices related to the major stage for AJCC T Stage.
    '''
    'is' = 'is', 'Tis'
    'x' = 'x', 'Tx'
    '0' = '0', 'T0'
    '1' = '1', 'T1'
    '1a' = '1a', 'T1a'
    '1b' = '1b', 'T1b'
    '1c' = '1c', 'T1c'
    '1d' = '1d', 'T1d'
    '2' = '2', 'T2'
    '2a' = '2a', 'T2a'
    '2b' = '2b', 'T2b'
    '2c' = '2c', 'T2c'
    '2d' = '2d', 'T2d'
    '3' = '3', 'T3'
    '3a' = '3a', 'T3a'
    '3b' = '3b', 'T3b'
    '3c' = '3c', 'T3c'
    '3d' = '3d', 'T3d'
    '4' = '4', 'T4'
    '4a' = '4a', 'T4a'
    '4b' = '4b', 'T4b'
    '4c' = '4c', 'T4c'
    '4d' = '4d', 'T4d'
    
class AJCCMajorNStageChoices(models.TextChoices):
    '''
    Enum to store choices related to the major stage for AJCC N Stage
    '''
    '0' = '0', 'N0'
    '1' = '1', 'N1'
    '1a' = '1a','N1a'
    '1b' = '1b','N1b'
    '1c' = '1c','N1c'
    '1d' = '1d','N1d'
    '2' = '2', 'N2'
    '2a' = '2a','N2a'
    '2b' = '2b','N2b'
    '2c' = '2c','N2c'
    '2d' = '2d','N2d'
    '3' = '3', 'N3'
    '3a'= '3a', 'N3a'
    '3b'= '3b', 'N3b'
    '3c'= '3c', 'N3c'
    '3d'= '3d', 'N3d'
    '4' = '4', 'N4'
    '4a' = '4a', 'N4a'
    '4b' = '4b', 'N4b'
    '4c' = '4c', 'N4c'
    '4d' = '4d', 'N4d'
    'x' = 'x', 'Nx'

class AJCCMajorMStageChoices(models.TextChoices):
    '''
    Enum to store choices related to major stage for AJCC M Stage
    '''
    '0' = '0', 'M0'
    '1' = '1', 'M1'
    '1a' = '1a', 'M1a'
    '1b' = '1b', 'M1b'
    '1c' = '1c', 'M1c'

class AJCCSuffixChoices(models.TextChoices):
    '''
    Enum to store choices related to suffix for AJCC T, N and M Stage.
    '''
    '(i+)' = 'i', 'isolated tumor cells'
    '(m)' = 'm', 'multifocal'
    '(mi)' = 'mi', 'micrometastasis'

class Diagnosis(models.Model):
    '''
    Model to store information about the diagnosis of the patient.
    '''
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,verbose_name = "Patient", help_text="Enter the patient's name")
    cancer_site = models.ForeignKey(LookupCancerSite,on_delete=models.CASCADE,verbose_name = "Primary Site of the Cancer", help_text="Enter the patient's primary cancer site. For example if the patient has been diagnosed with a brain metastases from a breast cancer, enter breast cancer here not brain metastases.")
    cancer_side = models.CharField(verbose_name = "Side of the Primary Cancer", help_text="Enter side where the primary cancer occured. Again this is the site of the primary disease not of the metastases",max_length=20,choices=CancerSideChoices.choices)
    cancer_pathology = models.ForeignKey(LookupPathology,on_delete=models.CASCADE,verbose_name = "Pathology of the Cancer", help_text="Enter the patient's primary cancer pathology.")
    date_of_diagnosis = models.DateField(verbose_name = "Date of Primary Diagnosis", help_text="Enter the patient's date of primary cancer diagnosis. Note that this date can be earlier than the date of present reason why radiotherapy is being administered.")
    ajcc_t_stage_prefix = models.CharField(verbose_name = "AJCC T Stage Prefix", help_text="Enter the AJCC T Stage Prefix",max_length=20,choices=AJCCStagePrefixChoices.choices,default='c')
    ajcc_t_stage_major = models.CharField(verbose_name = "AJCC T Stage Major", help_text="Enter the AJCC T Stage Major",max_length=20,choices=AJCCMajorTStageChoices.choices,default='0')
    ajcc_t_stage_suffix = models.CharField(verbose_name = "AJCC T Stage Suffix", help_text="Enter the AJCC T Stage Suffix",max_length=20,choices=AJCCSuffixChoices.choices,null=True,blank = True)
    ajcc_n_stage_prefix = models.CharField(verbose_name = "AJCC N Stage Prefix", help_text="Enter the AJCC N Stage Prefix",max_length=20,choices=AJCCStagePrefixChoices.choices,default='c')
    ajcc_n_stage_major = models.CharField(verbose_name = "AJCC N Stage Major", help_text="Enter the AJCC N Stage Major",max_length=20,choices=AJCCMajorNStageChoices.choices,default='0')
    ajcc_n_stage_suffix = models.CharField(verbose_name = "AJCC N Stage Suffix", help_text="Enter the AJCC N Stage Suffix",max_length=20,choices=AJCCSuffixChoices.choices,null=True,blank=True)
    ajcc_m_stage_prefix = models.CharField(verbose_name = "AJCC M Stage Prefix", help_text="Enter the AJCC M Stage Prefix",max_length=20,choices=AJCCStagePrefixChoices.choices,default='c')
    ajcc_m_stage_major = models.CharField(verbose_name = "AJCC M Stage Major", help_text="Enter the AJCC M Stage Major",max_length=20,choices=AJCCMajorMStageChoices.choices,default='0')
    ajcc_m_stage_suffix = models.CharField(verbose_name = "AJCC M Stage Suffix", help_text="Enter the AJCC M Stage Suffix",max_length=20,choices=AJCCSuffixChoices.choices,null=True,blank=True)
    overall_stage = models.CharField(verbose_name = "Overall Stage", help_text="Enter the Overall Stage",max_length=20,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name = "Created At", help_text="Enter Date Time when this patient's record was created")
    modified_at = models.DateTimeField(auto_now=True,verbose_name = "Modified At", help_text="Enter the Date Time when this patient's record was modified")
    
    class Meta:
        verbose_name = "Diagnosis"
        verbose_name_plural = "Diagnoses"
        constraints = [
            models.UniqueConstraint(
                fields=['patient', 'cancer_site', 'cancer_side', 'cancer_pathology'],
                name='unique_patient_cancer_site_side_pathology'
            )
        ]
    
    def __str__(self):
        return f"{self.patient.patient_uid} - {self.cancer_site}"

    def clean(self):
        super().clean()
        if self.patient.date_of_birth and self.date_of_diagnosis and self.patient.date_of_birth > self.date_of_diagnosis:
            raise ValidationError({
                "date_of_diagnosis": "Date of Diagnosis cannot be earlier than Date of Birth."
            })    

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class TreatmentIntentChoices(models.TextChoices):
    '''
    Enum to store choices related to the treatment intent.
    '''
    curative = 'curative', 'Curative'
    palliative = 'palliative', 'Palliative'

class TreatmentSequenceChoices(models.TextChoices):
    '''
    Enum to store choices related to Treatment Sequence.
    '''
    definitive = 'definitive', 'Definitive'
    adjuvant = 'adjuvant', 'Adjuvant'
    neoadjuvant = 'neoadjuvant', 'Neoadjuvant'
    prophylactic = 'prophylactic', 'Prophylactic'
    palliative = 'palliative', 'Palliative'
    


class RadiotherapyModalityChoices(models.TextChoices):
    '''
    Enum to store choices related to Radiotherapy Modality.
    '''
    EBRT = 'EBRT', 'External Beam Radiotherapy'
    BRT = 'BRT', 'Brachytherapy'
    


class RadiotherapyBooking(models.Model):
    '''
    Class to store information about the booking for the radiotherapy of the patient.
    '''
    diagnosis = models.ForeignKey(Diagnosis,on_delete=models.CASCADE,verbose_name = "Linked Diagnosis", help_text="Enter the diagnosis for the patient")
    radiotherapy_treatment_intent = models.CharField(verbose_name = "Radiotherapy Treatment Intent", help_text="Enter the treatment intent",max_length=30,choices=TreatmentIntentChoices)
    radiotherapy_treatment_sequence = models.CharField(verbose_name = "Radiotherapy Treatment Sequence", help_text="Enter the treatment sequence",max_length=30,choices=TreatmentSequenceChoices)
    radiotherapy_modality = models.CharField(verbose_name = "Radiotherapy Modality", help_text="Enter the radiotherapy modality",max_length=30,choices=RadiotherapyModalityChoices)
    radiotherapy_treatment_technique = models.ForeignKey(LookupRadiotherapyTreatmentTechnique,on_delete=models.CASCADE,verbose_name = "Radiotherapy Treatment Technique", help_text="Enter the radiotherapy treatment technique")
    radiotherapy_billing_category = models.ForeignKey(LookupBillingCode,on_delete=models.CASCADE,verbose_name = "Radiotherapy Billing Category", help_text="Enter the billing code")
    concurrent_systemic_therapy = models.BooleanField(verbose_name = "Concurrent Systemic Therapy Planned", help_text="Enter if concurrent systemic therapy is planned",default=False)
    systemic_therapy_type = models.ManyToManyField(LookupSystemicTherapyType,verbose_name = "Concurrent Systemic Therapy Type", help_text="Select the systemic therapy type(s) to be administered concurrently with radiotherapy")
    proposed_planning_image_date = models.DateField(verbose_name = "Proposed Planning Imaging Date", help_text="Enter the proposed date for radiotherapy planning",null=True,blank=True)
    proposed_treatment_start_date = models.DateField(verbose_name = "Proposed Treatment Start Date", help_text="Enter the proposed treatment start date",null=True,blank=True)
    planned_total_dose = models.DecimalField(verbose_name = "Planned Total Dose", help_text="Enter the planned total dose (Gy)",max_digits=5,decimal_places=2,default = 0,validators=[MaxValueValidator(300),MinValueValidator(0)])
    planned_total_number_of_fractions = models.IntegerField(verbose_name = "Planned Total Number of Fractions", help_text="Enter the planned total number of fractions",default = 1,validators=[MaxValueValidator(300),MinValueValidator(0)])
    planned_number_of_fractions_per_day = models.IntegerField(verbose_name = "Planned Number of Fractions per Day", help_text="Enter the planned number of fractions per day",null=True,blank=True,default = 1,validators=[MaxValueValidator(4),MinValueValidator(1)])
    planned_number_of_fractions_per_week = models.IntegerField(verbose_name = "Planned Number of Fractions per Week", help_text="Enter the planned number of fractions per week",null=True,blank=True,default =5,validators=[MaxValueValidator(28),MinValueValidator(1)])
    planned_dose_per_fraction = models.GeneratedField(
        verbose_name = "Planned Dose per Fraction",
        help_text="The planned dose per fraction",
        expression = "F('planned_total_dose') / F('planned_total_number_of_fractions')",
        output_field = models.DecimalField(max_digits=5,decimal_places=2)
    )
    planned_overall_treatment_duration = models.GeneratedField(
        verbose_name = "Planned Overall Treatment Duration in days",
        help_text="The planned overall treatment duration in days",
        expression = "(F('planned_total_number_of_fractions') * 7)/ F('planned_number_of_fractions_per_day')*F('planned_number_of_fractions_per_week')",
        output_field = models.IntegerField()
    )
    created_at = models.DateTimeField(auto_now_add=True,verbose_name = "Created At", help_text="Enter Date Time when this patient's record was created")
    modified_at = models.DateTimeField(auto_now=True,verbose_name = "Modified At", help_text="Enter the Date Time when this patient's record was modified")

    class Meta:
        verbose_name = "Radiotherapy Treatment Plan"
        verbose_name_plural = "Radiotherapy Treatment Plans"

    def __str__(self):
        return f"{self.diagnosis.patient.patient_uid} - {self.radiotherapy_modality}"

    def clean(self):
        super().clean()
        if self.proposed_treatment_start_date and self.diagnosis and self.diagnosis.date_of_diagnosis:
            if self.proposed_treatment_start_date < self.diagnosis.date_of_diagnosis:
                raise ValidationError({
                    "proposed_treatment_start_date": "Proposed Treatment Start Date cannot be earlier than Date of Diagnosis."
                })
        
        if self.proposed_planning_image_date and self.proposed_treatment_start_date:
            if self.proposed_planning_image_date > self.proposed_treatment_start_date:
                raise ValidationError({
                    "proposed_planning_image_date": "Proposed Planning CT Date cannot be later than Proposed Treatment Start Date."
                })
        
        if self.pk and not self.concurrent_systemic_therapy:
            if self.systemic_therapy_type.exists():
                raise ValidationError({
                    "systemic_therapy_type": "Systemic Therapy Type can only be selected when Concurrent Systemic Therapy is planned."
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

        

    
