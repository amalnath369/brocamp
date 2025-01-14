from django.urls import path
from . import views

urlpatterns=[
    path('adminindex',views.adminloginindex,name='adminindex'),
    path('adminlogin/',views.admin_login,name='adminlogin'),
    path('adminreg',views.adminreg,name='adminreg'),
    path('studform',views.studentregform,name='studform'),
    path('empform',views.employeeregform,name='empform'),
    path('admform',views.adminregform,name='admform'),
    path('studreg',views.StudentReg,name='studreg'),
    path('logout',views.logout,name='logout'),
    path('empreg',views.EmployeeReg,name='empreg'),
    path('adminforgot',views.forgotpasswordadmin,name='forgotadmin'),
    path('adminotp',views.admin_verify_otp,name='adminverify'),
    path('adminpassword',views.adminchangepassword,name='adminchangepassword'),
    path('admforgot',views.admforgot,name='forgotadm'),
    path('admemp',views.adm_employee,name='adminemp'),
    path('emplist/<str:dept>/',views.admemp_by_dept,name='emplist'),
    path('admstudent',views.admstudent,name='admstudent'),
    path('admbatch/<str:hub>/',views.admbatch_by_hub,name='admbatch'),
    path('admstudbybatch/<str:batch>/',views.admstudent_by_batch,name='admstudbatch'),
    path('edit/<str:id>/',views.editstudent,name='edit'),
    path('studupdate',views.studdetailedit,name='studupdate'),
    path('deletestud/<str:id>/',views.delete_student,name='delete'),
    path('ediemp/<str:id>/',views.editemp,name='editemp'),
    path('empupdate',views.Emp_detail_edit,name='empupdate'),
    path('deleteemp/<str:id>/',views.delete_emp,name='deleteemp')

]