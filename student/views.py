from django.shortcuts import render,redirect,HttpResponse
from rest_framework.decorators import api_view
from student.models import *
from django.contrib.auth.hashers import check_password,make_password
from student.serializer import *
from student.decorators import login_required
import random
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime

# Create your views here.
def index(request):
      return render(request,'login.html')

@login_required
def student(request):
      try:
            obj=request.session.get('employee_data')
            if obj:
                  hub=StudentData.objects.values_list('hub',flat=True).distinct()
                  return render(request,'student.html',{'obj':obj,'hub':hub})
            else:
                  return redirect('emplogin')
      except Exception as e:
                  return HttpResponse({'error':str(e)})

@api_view(['GET', 'POST'])
def EmployeeLogin(request):
      if request.method=='GET':
            return render(request,'login.html')      

      if request.method=='POST':
            empid=request.data.get('Empid')
            password=request.data.get('password')
            if not empid or not password:
                   return render(request,'login.html',{'error':'Employee ID and Password Required'})
            try:
                  obj=EmployeeData.objects.filter(Empid=empid).first()
                  if obj:
                       if check_password(password,obj.password):
                             serializer = employeeserializer(obj)
                             request.session['employee_data'] = {
                        'name': obj.Name,
                        'empid': obj.Empid,
                        'worklocation': obj.Work_location,
                        'designation': obj.Designation
                        }
                             print(request.session['employee_data'])
                             return render(request,'dashboard.html',{'obj': request.session['employee_data']})                         
                       else:
                          return render(request,'login.html',{'error':'Invalid Password'})                             
                  else:
                     return render(request,'login.html',{'error':'Invalid Employee ID'})
            except Exception as e:
                  return render(request,'login.html',{'error': str(e)})


@login_required
def batch_by_hub(request,hub):
   try:
      obj=request.session.get('employee_data')
      batch=StudentData.objects.filter(hub=hub).values_list('batch',flat=True).distinct()
      return render(request,'batches.html',{'batch':batch,'obj':obj})
   except Exception as e:
        return HttpResponse({'error':str(e)})
   
@login_required
def student_by_batch(request,batch):
   try:
      student=StudentData.objects.filter(batch=batch)
      return render(request,'studentlist.html',{'student':student})
   except Exception as e:
        return HttpResponse({'error':str(e)})
   
@login_required
def logout(request):
      if 'employee_data' in request.session:
            del request.session['employee_data']  
      return render(request, 'login.html') 


def forgotpassword(request):
        emp = request.POST.get('empid')
        print(emp) 
        try:

            obj = EmployeeData.objects.get(Empid=emp)
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session['empid'] = emp
            otp_expiry= timezone.now() + timezone.timedelta(minutes=5) 
            request.session['otp_expiry']=otp_expiry.isoformat()      
            subject = 'OTP for Password Change'
            message = f"""Dear {obj.Name},
                You requested a password change for your account. Please use the following One-Time Password (OTP) to proceed:
                
                OTP: {otp}
                
                This OTP is valid for the next 10 minutes.
                Thank You
                Team Brocamp"""
            
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [obj.email], fail_silently=True)
                return render(request,'otpenter.html')
            except Exception as e:
                return HttpResponse(f"An error occurred while sending the email: {str(e)}", status=500)
        except EmployeeData.DoesNotExist:
            return HttpResponse("User not found.", status=404)
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)
        
def verify_otp(request):
        otp_digits = request.POST.getlist('otp[]')  
        print(otp_digits)
        entered_otp = ''.join(otp_digits)
        print(entered_otp)
        created_otp = request.session.get('otp')
        otp_expiry_str = request.session.get('otp_expiry')
        
        if created_otp is None or otp_expiry_str is None:
            return render(request, 'otpenter.html', {'error': 'OTP expired or invalid. Please request a new one.'})
        otp_expiry=datetime.fromisoformat(otp_expiry_str)
        if timezone.now() > otp_expiry:
            return render(request, 'otpenter.html', {'error': 'OTP expired or invalid. Please request a new one.'})
        

        if str(entered_otp) == str(created_otp):
            return render(request,'passwordchange.html')
        else:
            return render(request, 'otpenter.html', {'error': 'Invalid OTP! Please try again.'})

def changepassword(request):
      if request.method=="POST":
         newpass=request.POST.get('new_password')  
         confpass=request.POST.get("confirm_password")
         if newpass!=confpass:
              return render(request,'passwordchange.html',{'error':'Passwords do not Match'})
         else:
              emp=request.session.get('empid')
              if not emp:
                  return render(request,'passwordchange.html',{'error':'Session Expired'})

              try:
                   obj=EmployeeData.objects.get(Empid=emp)
                   if obj:
                        hash_pass=make_password(confpass)
                        obj.password=hash_pass
                        obj.save()
                        return render(request,'login.html')
              except EmployeeData.DoesNotExist:
                  return render(request,'passwordchange.html',{'error':'Employee not found'})
              except Exception as e:
                  return render(request,'passwordchange.html',{'error':f'An error occured {str(e)}'})

                     
      else:     
        return render(request, 'otpenter.html', {'error': 'Invalid action.'})

       

def forgot(request):
      return render(request,'otpempid.html')


@login_required
def employee(request):
      try:
            obj=request.session.get('employee_data')
            if obj:
                  dept=EmployeeData.objects.values_list('Dept',flat=True).distinct()
                  return render(request,'emp.html',{'obj':obj,'dept':dept})
            else:
                  return redirect('emplogin')
      except Exception as e:
                  return HttpResponse({'error':str(e)})


@login_required
def emp_by_dept(request,dept):
   try:
      emp=EmployeeData.objects.filter(Dept=dept)
      return render(request,'admdept.html',{'emp':emp})
   except Exception as e:
        return HttpResponse({'error':str(e)})