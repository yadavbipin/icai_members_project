from django.db import models

# Create your models here.
class Personal_Info(models.Model):
    id=models.AutoField(primary_key=True)
    member_firstname = models.CharField(max_length=100,blank=True, null=True)
    member_lastname = models.CharField(max_length=100,blank=True, null=True,default='')
    membership_number=models.CharField(max_length=100,blank=True, null=True)
    year_of_membership=models.CharField(max_length=100,blank=True, null=True)
    Phone_number=models.CharField(max_length=20,blank=True, null=True)
    photo=models.ImageField(upload_to='Info_App/images/',default='',blank=True, null=True)  
    prof_address = models.CharField(max_length=500,blank=True, null=True)
    prof_area = models.CharField(max_length=500,blank=True, null=True)
    prof_city = models.CharField(max_length=500,blank=True, null=True)
    prof_pin_code = models.CharField(max_length=100,blank=True, null=True)
    residential_address = models.CharField(max_length=500,blank=True, null=True)
    residential_area = models.CharField(max_length=500,blank=True, null=True)
    residential_city = models.CharField(max_length=500,blank=True, null=True)
    residential_pin_code = models.CharField(max_length=100,blank=True, null=True)
    blood_group=models.CharField(max_length=10,blank=True, null=True)
    DOB=models.DateField(blank=True, null=True)
    DOM=models.DateField(blank=True, null=True)
    email_id = models.EmailField(max_length=100,blank=True, null=True)
    organization=models.CharField(max_length=500,blank=True, null=True)
    holding_COP=models.CharField(max_length=100,blank=True, null=True)
   
    # created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return self.member_firstname
    
    
Holding_COP = (
   ('Y', 'Yes'),
   ('N', 'No')
)
class form_submission(models.Model):
    id=models.AutoField(primary_key=True)
    member_firstname = models.CharField(max_length=100,blank=True, null=True)
    member_lastname = models.CharField(max_length=100,blank=True, null=True,default='')
    membership_number=models.CharField(max_length=100,blank=True, null=True)
    year_of_membership=models.CharField(max_length=100,blank=True, null=True)
    Phone_number=models.CharField(max_length=100,blank=True, null=True)
    photo=models.ImageField(upload_to='Info_App/image/',default='',blank=True, null=True)  
    prof_address = models.CharField(max_length=500,blank=True, null=True)
    prof_area = models.CharField(max_length=500,blank=True, null=True)
    prof_city = models.CharField(max_length=500,blank=True, null=True)
    prof_pin_code = models.CharField(max_length=100,blank=True, null=True)
    residential_address = models.CharField(max_length=500,blank=True, null=True)
    residential_area = models.CharField(max_length=500,blank=True, null=True)
    residential_city = models.CharField(max_length=500,blank=True, null=True)
    residential_pin_code = models.CharField(max_length=100,blank=True, null=True)
    corr_prof_address = models.CharField(max_length=500,blank=True, null=True, default=" ")
    corr_prof_area = models.CharField(max_length=500,blank=True, null=True, default=" ")
    corr_prof_city = models.CharField(max_length=500,blank=True, null=True, default=" ")
    corr_prof_pin_code = models.CharField(max_length=100,blank=True, null=True, default=" ")
    blood_group=models.CharField(max_length=10,blank=True, null=True)
    DOB=models.DateField(blank=True, null=True)
    DOM=models.DateField(blank=True, null=True)
    email_id = models.EmailField(max_length=100,blank=True, null=True)
    organization=models.CharField(max_length=500,blank=True, null=True)
    holding_COP = models.CharField(choices=Holding_COP, max_length=100)
   
    # created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return self.member_firstname

