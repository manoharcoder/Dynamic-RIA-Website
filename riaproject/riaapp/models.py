from django.db import models
from ckeditor.fields import RichTextField
# from django.db.models import Star
# Create your models here.

class Cources(models.Model):
    courseName=models.CharField(max_length=150)
    image=models.ImageField(upload_to='course',blank=True,null=True)
    courseFee=models.IntegerField()
    courseDuration=models.IntegerField()
    rating = models.FloatField(default=0)
    syllabus=RichTextField(default='syllabus')
    aboutCourse=RichTextField(default='aboutCourse')
    def __str__(self):
        return self.courseName
    


class Trainer(models.Model):
    trainer_name=models.CharField(max_length=50)
    trainer_designation=models.CharField(max_length=100)
    trainer_experience=models.DecimalField(max_digits=5,decimal_places=2)
    course=models.ForeignKey(Cources,on_delete=models.SET_NULL, null=True)
    def __str__(self):
       return self.trainer_name



class Register(models.Model):
    candidateId=models.AutoField(primary_key=True)
    firstName=models.CharField(max_length=20)
    lastName=models.CharField(max_length=20)
    fatherName=models.CharField(max_length=20)
    phoneNumber=models.IntegerField()
    alternateNumber=models.IntegerField()
    email=models.EmailField(unique=True)
    collegeName=models.CharField(max_length=100)
    address=models.TextField(max_length=150)
    landMark=models.CharField(max_length=100)
    street=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    pincode=models.IntegerField()
    companyName=models.CharField(max_length=150,blank=True,null=True)
    designation=models.CharField(max_length=150)
    qualification=models.CharField(max_length=100)
    computerKnowledge=models.CharField(max_length=50)
    course=models.TextField(max_length=350,blank=True,null=True)
    timeStamp=models.DateField(auto_now_add=True)
    trainer=models.ForeignKey(Trainer,on_delete=models.DO_NOTHING,null=True)
    
    def __str__(self):
        return self.email
    

class Payments(models.Model):
    name=models.ForeignKey(Register,on_delete=models.CASCADE)
    amountPaid=models.IntegerField()
    balance=models.IntegerField(blank=True,null=True)
    status=models.CharField(max_length=20,default="Unpaid")
   
    def __str__(self):
        return self.status

    
class Documents(models.Model):
    email=models.ForeignKey(Register,on_delete=models.CASCADE)
    document=models.ImageField(upload_to='documents')
    verification=models.BooleanField(default=False)

    def __str__(self):
        return self.email
    

class Certificate(models.Model):
    email=models.ForeignKey(Register,on_delete=models.CASCADE)
    Certificate=models.ImageField(upload_to='certificates')

    def __str__(self):
       return self.email



class Contact(models.Model):
    name=models.CharField(max_length=25)
    email=models.EmailField()
    phoneNumber=models.CharField(max_length=12)
    description=models.TextField(max_length=250)
    def __str__(self):
        return self.email
   

class Attendance(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    date=models.CharField(max_length=50)
    logintime=models.CharField(max_length=50)
    logouttime=models.CharField(max_length=50)
    approvalstatus=models.BooleanField(default=False)
    def __str__(self):
        return self.email
    


