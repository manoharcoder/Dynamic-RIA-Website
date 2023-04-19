from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
import re

from riaapp.models import Cources,Register,Contact,Payments,Attendance


from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# Create your views here.
def Home(request):
    return render(request,"home.html")

def handleSignin(request):
    if request.method=='POST':
        flag=0
        userName=request.POST['name']
        userEmail=request.POST['email']
        userPassword=request.POST['pass1']
        userConfirmPassword=request.POST['pass2']
        # password validations field
        if userPassword!=userConfirmPassword:
            messages.warning(request,'password not match with cnfirm password')
            return redirect("/signin")

        if len(userPassword)<8:
            messages.warning(request,'password length must be graterthan or equeal  to 8 characters ')
            return redirect('/signin')
        elif not re.search('[A-Z]',userPassword):
            flag=-1
        elif not re.search('[a-z]',userPassword):
            flag=-1
        elif not re.search('[0-9]',userPassword):
            flag=-1
        elif not re.search('[_@$]',userPassword):
           flag=-1
        else:    
             messages.success(request,' Your Password is Valid')

      
        # elif not re.search('[A-Z]',userPassword):
        #     messages.info(request,'password must be includes in between A-Z')
        #     return redirect('/signin')

        # elif not re.search('[a-z]',userPassword):
        #     messages.info(request,'password must be includes in between a-z')
        #     return redirect('/signin')

        # elif not re.search('[0-9]',userPassword):
        #     messages.info(request,'password must be includes in between 0-9')
        #     return redirect('/signin')

        # elif not re.search('[_@$]',userPassword):
        #     messages.info(request,'password must be includes in between _@$')
        #     return redirect('/signin')
        # else:          

            # messages.success(request,' Your Password is Valid')
            # return redirect('/signin')
        if (flag==0):
            # logic for back end starts from here 
            try:
               if User.objetcts.get(userName=userEmail):
                messages.info(request,"Email is already taken")
                return redirect('/signin')


            except Exception as identifire :
                pass
            user=User.objects.create_user(userEmail,userEmail,userPassword)
           
            user.first_name=userName
            user.is_active=False        
            user.save()

            email_subject="Activate Your Account"
            message=render_to_string('activate.html',{
                'user':user,
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generate_token.make_token(user)

            })

            #email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            #email_message.send()
            # messages.success(request,f"Activate Your Account by clicking the link in your gmail {message}")
            messages.success(request,f"{message}") 
            return redirect('/login')
        else:
            messages.error(request, "password not valid")
            return redirect('/signin')


        # messages.info(request,f'{userName},{userEmail},{userPassword},{userConfirmPassword}') 
    return render(request,"signin.html")


class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(request,"Account Activated Successfully")
            messages.info(request,'please login to proceed  in to enroll page')
            return redirect('/login')
        return render(request,'activatefail.html')






def handleLogin(request):
  
    if request.method=="POST":
        userName=request.POST['email']
        userPassword=request.POST['pass1']

        myuser=authenticate(username=userName,password=userPassword)
        # myuser=User.objects.filter(username=username)
        print(userName,userPassword,myuser)
        if myuser is not None:
            login(request,myuser)
            messages.success(request,f'Login success as {request.user.email}')
            return redirect('/enroll')
        else:
            messages.error(request,"Invalid crentials")
            return redirect('/login')

    return render(request,'login.html')


       

def handleLogout(request):
    logout(request)
    messages.success(request,f'Logout success as {{User.email}}')
    return render(request,'login.html')

class RequestResetEmailView(View):

    def get(self,request):
        return render(request,'request-reset-email.html')

    def post(self,request):

        email=request.POST['email']
        user=User.objects.filter(email=email)


        if user.exists():
            # current_site=get_current_site(request)
            email_subject='[Reset Your Password]'
            message=render_to_string('reset-user-password.html',{
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0])
            })

            # email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            # email_message.send()

            messages.info(request,f"{message} " )
            return render(request,'request-reset-email.html')
        else:
            messages.error(request,'No Account Exists with this email' )
            return render(request,'request-reset-email.html')


def handleEnroll(request):


#    to set condition that is before enroll youn must be signup and also do login
      
    if not request.user.is_authenticated:
        messages.warning(request,'please do signup and login ')
        return redirect('/signin')


    cources=Cources.objects.all()
    context={'cources':cources}
    if request.method=='POST':
        fristName=request.POST.get('fname')
        lastName=request.POST.get('lname')
        fatherName=request.POST.get('fathername')
        phone=request.POST.get('phone')
        alternatePhone=request.POST.get('aphone')
        email=request.POST.get('email')
        collegeName=request.POST.get('college')
        doorNo=request.POST.get('doorno')
        street=request.POST.get('street')
        pinCode=request.POST.get('pincode')
        landMark=request.POST.get('landmark')
        city=request.POST.get('city')
        companyName=request.POST.get('companyname')
        designation=request.POST.get('designation')
        qualification=request.POST.get('qualification')
        level=request.POST.get('level')
        scourse=request.POST.get('scourse')
        ccourse=request.POST.get('ccourse')


        if scourse==ccourse:
            pass
        else:
            messages.info(request,'selected course and confirm course must be match')
            return redirect('/enroll')
        

        if 9<(len(phone) & len(alternatePhone))<13:
            pass
        else:
            messages.info(request,'must be phone number 10 digits for forners it should be 12 numbers')
            return redirect('/enroll')
        
        emailExist=Register.objects.filter(email=email)
        if emailExist:
            messages.error(request,'email is alredy taken provide another email to enroll')
            return redirect('/enroll')

        myquery=Register(firstName=fristName,lastName=lastName,fatherName=fatherName,phoneNumber=phone,alternateNumber=alternatePhone,email=email,collegeName=collegeName,address=doorNo,street=street,pincode=pinCode,landMark=landMark,city=city,companyName=companyName,designation=designation,qualification=qualification,computerKnowledge=level,course=scourse)
        myquery.save()
        # print(myquery.candidateId)
        messages.success(request,f"Enrollment Success with {request.user.email}")
        # print(fristName,lastName,fatherName,phone,alternatePhone,email,doorNo,street,pinCode,landMark,landMark,city,companyName,designation,qualification,level,scourse)
  


    return render(request,'enroll.html',context)



def course(request):
    cources=Cources.objects.all() 
    context={'cources':cources}
    return render(request,'course.html',context)






def handleDetails(request,id):
    cources=Cources.objects.filter(id=id)
    context={'cources':cources}
    return render(request,'deatils.html',context)




def handleContact(request):
    
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phoneNum=request.POST.get('num')
        description=request.POST.get('desc')
        query=Contact(name=name,email=email,phoneNumber=phoneNum,description=description)
        query.save()
        messages.success(request,"Thanks for Contacting us we will get back you soon...")
        return render(request,'contact.html')
      

    return render(request,'contact.html')



def candidateProfile(request):
        
    if not request.user.is_authenticated:
        messages.warning(request,'please do signup and login ')
        return redirect('/signin')

    currentuser=request.user.email
    # print(currentuser)
    query=Register.objects.filter(email=currentuser)
    payment=Payments.objects.all()
    paymentstatus=''
    amount=0
    balance=0
    for p in payment:
        if str(p.name)==currentuser:
            # print(p.name,type(str(p.name)))
            # print('matching')
            paymentstatus=p.status
            amount=p.amountPaid
            balance=p.balance
    # print(paymentstatus)
    # print(amount)
    # print(balance)
    paymentstats={'paymentstatus':paymentstatus,'amount':amount,'balance':balance}
    attendanceStats=Attendance.objects.filter(email=currentuser)
    context={'query':query,'paymentstats':paymentstats,'attendanceStats':attendanceStats}
    return render(request,'profile.html',context)




def attendance(request):   
    if not request.user.is_authenticated:
        messages.warning(request,'please do login and apply attendance ')
        return redirect('/login')
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        date=request.POST['date']
        logintime=request.POST['logintime']
        logouttime=request.POST['logouttime']
        query=Attendance(name=name,email=email,date=date,logintime=logintime,logouttime=logouttime)
        query.save()
        messages.success(request,'Applied Attendance Sucessfully Please Wait For Approval')
        return redirect('/candidateprofile')
    

    return render(request,'attendance.html')




def candidateupdate(request,id):
    mycrud=Register.objects.get(candidateId=id)
    makecrud=Cources.objects.all()
    if request.method=='POST':
        firstName=request.POST.get('fname')
        lastName=request.POST.get('lname')
        fatherName=request.POST.get('fathername')
        phone=request.POST.get('phone')
        alternatePhone=request.POST.get('aphone')
        collegeName=request.POST.get('college')
        doorNo=request.POST.get('doorno')
        street=request.POST.get('street')
        pinCode=request.POST.get('pincode')
        landMark=request.POST.get('landmark')
        city=request.POST.get('city')
        companyName=request.POST.get('companyname')
        designation=request.POST.get('designation')
        qualification=request.POST.get('qualification')
        scourse=request.POST.get('scourse')
        ccourse=request.POST.get('ccourse')
        # print(firstName,lastName,fatherName,phone,alternatePhone,email,collegeName,doorNo,street,pinCode,landMark,landMark,city,companyName,designation,qualification,level,scourse,ccourse)
        edit=Register.objects.get(candidateId=id)
        edit.firstName=firstName
        edit.lastName=lastName
        edit.fatherName=fatherName
        edit.phoneNumber=phone
        edit.alternateNumber=alternatePhone
        edit.collegeName=collegeName
        edit.address=doorNo
        edit.landMark=landMark
        edit.street=street
        edit.city=city
        edit.pincode=pinCode
        edit.companyName=companyName
        edit.designation=designation
        edit.qualification=qualification
        edit.course=scourse
        edit.save()
        messages.info(request,'data updated sucessfully')
        return redirect('/candidateprofile')
   
    
    context={'mycrud':mycrud,'makecrud':makecrud}
    return render(request,'update.html',context)


def deleteCandidate(request,id):
        
    return render(request,'signin.html')



