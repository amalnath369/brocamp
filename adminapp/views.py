from django.shortcuts import render,redirect,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password,make_password
from adminapp.models import *
from adminapp.serializer import *
from student.models import *
from adminapp.decorators import login_require
import random
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime
from django.conf import settings

def adminloginindex(request):
      return render(request,'adminlogin.html')
@api_view(['GET',"POST"])
def admin_login(request):
      if request.method=='GET':
            return render(request,'adminlogin.html')
            
      if request.method=="POST":
            empid=request.data.get('empid')
            password=request.data.get('password')
            if not empid or not password:
                   return Response({'error':'Employee ID and Password Required'})
            try:
                  obj=admin_data.objects.filter(empid=empid).first()
                  if obj:
                       if check_password(password,obj.password):
                             serializer = adminserialiser(obj)
                             request.session['admin_data'] = {
                        'name': obj.name,
                        'empid': obj.empid,
                        }
                             print(request.session['admin_data'])
                             return render(request,'admindashboard.html',{'obj': request.session['admin_data']})
                          
                       else:
                            return Response({'error':'Invalid Password'}) 
                  else:
                     return Response({'error':'Invalid Employee ID'})
            except Exception as e:
                  return Response({'error': str(e)})
@api_view(['POST'])
@login_require
def EmployeeReg(request):
      if request.method=='POST':
            name=request.data.get('Name')
            dept=request.data.get('Dept')
            empid=request.data.get('Empid')
            worklocation=request.data.get('Work_location')
            designation=request.data.get('Designation')
            password=request.data.get('password')
            phone=request.data.get('phonenumber')
            email=request.data.get('email')
            if not name or not dept or not empid or not password or not phone:
                 return render(request,'employeeregister.html',{'error':'All Fields are required'})
            try:
                obj=EmployeeData.objects.filter(Empid=empid).first()
                if obj:
                      return render(request,'employeeregister.html',{'error':'Employee Already exists'})
                else:
                    hash_password=make_password(password)
                    emp_obj=EmployeeData.objects.create(
                         Name=name,
                         Empid=empid,
                         Dept=dept,
                         password=hash_password,
                         phonenumber=phone,
                         Work_location=worklocation,
                         Designation=designation,
                         email=email
                    )
                    emp_obj.save()
                    return render(request,'employeeregister.html',{'message': 'Employee registered successfully'})
            except Exception as e:
                   return Response({'error':str(e)})
            

            
@api_view(['POST'])
@login_require
def adminreg(request):
      if request.method=='POST':
            name=request.data.get('name')
            empid=request.data.get('empid')
            password=request.data.get('password')
            phone=request.data.get('phonenumber')
            email=request.data.get('email')
            if not name or  not empid or not password or not phone or not email:
                 return render(request,'adminregister.html',{'error':'All Fields are required'})
            try:
                obj=admin_data.objects.filter(empid=empid).first()
                if obj:
                      return render(request,'adminregister.html',{'error':'Employee Already exists'})
                else:
                    hash_password=make_password(password)
                    adm_obj=admin_data.objects.create(
                         name=name,
                         empid=empid,
                         password=hash_password,
                         phonenumber=phone,
                         email=email
                    )
                    adm_obj.save()
                    return render(request,'adminregister.html',{'message': 'Admin registered successfully'})
            except Exception as e:
                   return render(request,'adminregister.html',{'error':str(e)})

@login_require
def studentregform(request):
      return render(request,'studentregister.html')

@login_require
def employeeregform(request):
      return render(request,'employeeregister.html')

@login_require
def adminregform(request):
      return render(request,'adminregister.html')

@api_view(['POST'])
@login_require
def StudentReg(request):
            name=request.data.get('name')
            hub=request.data.get('hub')
            batch=request.data.get('batch')
            domain=request.data.get('domain')
            student_number=request.data.get('phonenumber')
            guardian_number=request.data.get('guardiannumber')
            guardianname=request.data.get('guardianname')
            email=request.data.get('email')
            mentor=request.data.get('mentor')
            if not name or not batch or not domain or not student_number or not guardian_number or not email or not hub:
                  return render(request,'studentregister.html',{'error':'All Fields are Required'})
            HUB_CHOICES = ['BCK', 'BCE', 'BCT', 'BCB', 'BCR','BCCH','BCCO']
            if hub not in HUB_CHOICES:
               return render(request,'studentregister.html',{'error': 'Invalid Hub'}, status=400)

            try:
                obj=StudentData.objects.filter(email=email).first()
                if obj:
                      return render(request,'studentregister.html',{'error':'student Already exists'})

                mentor_obj=EmployeeData.objects.filter(Empid=mentor).first()
                if not mentor_obj:
                      return render(request,'studentregister.html',{'error':'Employee ID not Found'})
                
                stud_obj=StudentData.objects.create(
                         name=name,
                         batch=batch,
                         domain=domain,
                         phonenumber=student_number,
                         guardiannumber=guardian_number,
                         email=email,
                         hub=hub,
                         guardianname=guardianname,
                         mentor=mentor_obj
                    )
                stud_obj.save()
                return render(request,'studentregister.html',{'message': 'Student registered successfully'})
            except Exception as e:
                   return render(request, 'studentregister.html', {'error': str(e)})
@login_require
def logout(request):
      if 'admin_data' in request.session:
            del request.session['admin_data']
      return  render(request,'adminlogin.html')

def forgotpasswordadmin(request):
        emp = request.POST.get('empid')
        print(emp) 
        try:

            obj = admin_data.objects.get(empid=emp)
            otp = random.randint(100000, 999999)
            print(otp)
            request.session['otp'] = otp
            request.session['empid'] = emp
            otp_expiry= timezone.now() + timezone.timedelta(minutes=5) 
            request.session['otp_expiry']=otp_expiry.isoformat()      
            subject = 'OTP for Password Change'
            message = f"""Dear {obj.name},
                You requested a password change for your account. Please use the following One-Time Password (OTP) to proceed:
                
                OTP: {otp}
                
                This OTP is valid for the next 10 minutes.
                Thank You
                Team Brocamp"""
            
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [obj.email], fail_silently=True)
                return render(request,'adminotpenter.html')
            except Exception as e:
                return HttpResponse(f"An error occurred while sending the email: {str(e)}", status=500)
        except EmployeeData.DoesNotExist:
            return HttpResponse("User not found.", status=404)
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)
        
def admin_verify_otp(request):
        otp_digits = request.POST.getlist('otp[]')  
        print(otp_digits)
        entered_otp = ''.join(otp_digits)
        print(entered_otp)
        created_otp = request.session.get('otp')
        otp_expiry_str = request.session.get('otp_expiry')
        
        if created_otp is None or otp_expiry_str is None:
            return render(request, 'adminotpenter.html', {'error': 'OTP expired or invalid. Please request a new one.'})
        otp_expiry=datetime.fromisoformat(otp_expiry_str)
        if timezone.now() > otp_expiry:
            return render(request, 'adminotpenter.html', {'error': 'OTP expired or invalid. Please request a new one.'})
        

        if str(entered_otp) == str(created_otp):
            return render(request,'adminpasswordchange.html')
        else:
            return render(request, 'adminotpenter.html', {'error': 'Invalid OTP! Please try again.'})

def adminchangepassword(request):
      if request.method=="POST":
         newpass=request.POST.get('new_password')  
         confpass=request.POST.get("confirm_password")
         if newpass!=confpass:
              return render(request,'adminpasswordchange.html',{'error':'Passwords do not Match'})
         else:
              emp=request.session.get('empid')
              if not emp:
                  return render(request,'adminpasswordchange.html',{'error':'Session Expired'})

              try:
                   obj=admin_data.objects.get(empid=emp)
                   if obj:
                        hash_pass=make_password(confpass)
                        obj.password=hash_pass
                        obj.save()
                        return render(request,'adminlogin.html')
              except EmployeeData.DoesNotExist:
                  return render(request,'adminpasswordchange.html',{'error':'Employee not found'})
              except Exception as e:
                  return render(request,'adminpasswordchange.html',{'error':f'An error occured {str(e)}'})

                     
      else:     
        return render(request, 'adminotpenter.html', {'error': 'Invalid action.'})


def admforgot(request):
      return render(request,'adminotpemp.html')


@login_require
def adm_employee(request):
      try:
            obj=request.session.get('admin_data')
            if obj:
                  dept=EmployeeData.objects.values_list('Dept',flat=True).distinct()
                  request.session['dept']=list(dept)
                  return render(request,'admemp.html',{'obj':obj,'dept':dept})
            else:
                  return redirect('adminlogin')
      except Exception as e:
                  return HttpResponse({'error':str(e)})


@login_require
def admemp_by_dept(request,dept):
   try:
      emp=EmployeeData.objects.filter(Dept=dept)
      return render(request,'dept.html',{'emp':emp})
   except Exception as e:
        return HttpResponse({'error':str(e)})
   

@login_require
def admstudent(request):
      try:
            obj=request.session.get('admin_data')
            if obj:
                  hub=StudentData.objects.values_list('hub',flat=True).distinct()
                  return render(request,'admstudent.html',{'obj':obj,'hub':hub})
            else:
                  return redirect('adminlogin')
      except Exception as e:
                  return HttpResponse({'error':str(e)})
      

@login_require
def admbatch_by_hub(request,hub):
   try:
      obj=request.session.get('admin_data')
      batch=StudentData.objects.filter(hub=hub).values_list('batch',flat=True).distinct()
      
      return render(request,'admbatches.html',{'batch':batch,'obj':obj})
   except Exception as e:
        return HttpResponse({'error':str(e)})
   
@login_require
def admstudent_by_batch(request,batch):
   try:
      student=StudentData.objects.filter(batch=batch)
      return render(request,'admstudentlist.html',{'student':student})
   except Exception as e:
        return HttpResponse({'error':str(e)})
   

@login_require
def editstudent(request,id):
         try:
              obj=StudentData.objects.get(name=id)
              return render(request,'edit.html',{'id':obj})
         except Exception as e:
              return HttpResponse({'error':str(e)})                   


@login_require
def studdetailedit(request):
      if request.method=='POST':
            id=request.POST.get('id')
            name=request.POST.get('name')
            hub=request.POST.get('hub')
            batch=request.POST.get('batch')
            domain=request.POST.get('domain')
            student_number=request.POST.get('phonenumber')
            guardian_number=request.POST.get('guardiannumber')
            guardianname=request.POST.get('guardianname')
            email=request.POST.get('email')
            mentor=request.POST.get('mentor')
            if not name or not batch or not domain or not student_number or not guardian_number or not email or not hub:
                  return render(request,'edit.html',{'error':'All Fields are Required'})
            HUB_CHOICES = ['BCK', 'BCE', 'BCT', 'BCB', 'BCR','BCCH','BCCO']
            if hub not in HUB_CHOICES:
               return render(request,'edit.html',{'error': 'Invalid Hub'}, status=400)

            try:
                mentor_obj=EmployeeData.objects.filter(Empid=mentor).first()
                if not mentor_obj:
                      return render(request,'edit.html',{'error':'Employee ID not Found'})
                
                stud_obj=StudentData.objects.get(id=id)
                if stud_obj:
                     stud_obj.name=name
                     stud_obj.hub=hub
                     stud_obj.batch=batch
                     stud_obj.domain=domain
                     stud_obj.email=email
                     stud_obj.phonenumber=student_number
                     stud_obj.guardianname=guardianname
                     stud_obj.guardiannumber=guardian_number
                     stud_obj.mentor=mentor_obj
                     stud_obj.save()
                     return render(request,'edit.html',{'message': 'Details Editted successfully'})
            except Exception as e:
                   return render(request, 'edit.html', {'error': str(e)})

@login_require
def delete_student(request,id):
       try:
             obj=StudentData.objects.get(name=id)
             if obj:
                  obj.delete()
                  return render(request,'admstudentlist.html')
       except Exception as e:
            return HttpResponse({'error':str(e)})
     
@login_require
def editemp(request,id):
         try:
              print(id)
              obj=EmployeeData.objects.get(Empid=id)
              return render(request,'empedit.html',{'id':obj})
         except Exception as e:
              return HttpResponse({'error':str(e)})                   


@login_require
def Emp_detail_edit(request):
      if request.method=='POST':
            id=request.POST.get('id')
            name=request.POST.get('Name')
            dept=request.POST.get('Dept')
            worklocation=request.POST.get('Work_location')
            designation=request.POST.get('Designation')
            phone=request.POST.get('phonenumber')
            email=request.POST.get('email')
            if not name or not dept  or not phone:
                 return render(request,'empedit.html',{'error':'All Fields are required'})
            try:

                    emp_obj=EmployeeData.objects.get(Empid=id)
                    emp_obj.Name=name
                    emp_obj.Dept=dept
                    emp_obj.Work_location=worklocation
                    emp_obj.Designation=designation
                    emp_obj.phonenumber=phone
                    emp_obj.email=email
                    emp_obj.save()
                    return render(request,'empedit.html',{'message': 'Employee registered successfully'})
            except EmployeeData.DoesNotExist:
                   return render(request, 'empedit.html', {'error': 'Employee not found.'})
            except Exception as e:
                   return HttpResponse({'error':str(e)})


@login_require
def delete_emp(request, id):
    try:
        obj = EmployeeData.objects.get(Empid=id)
        obj.delete()
        dept=request.session.get('dept')
        return redirect('emplist',dept)
    except EmployeeData.DoesNotExist:
        return HttpResponse(f"Employee with ID {id} does not exist.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
