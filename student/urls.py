from django.urls import path
from student import views

urlpatterns=[
    path('',views.index,name='index'),
    # path('dashboard/',views.dashboard,name='dashboard'),
    path('emplogin/', views.EmployeeLogin,name='emplogin'),
    path('studenthub',views.student,name='student'),
    path('batch/<str:hub>/',views.batch_by_hub,name='batchs'),
    path('student/<str:batch>/',views.student_by_batch,name='students'),
    path('logout',views.logout,name='logout'),
    path('forgotpass',views.forgotpassword,name='forgotpassword'),
    path('forgot',views.forgot,name='forgot'),
    path('verifyotp',views.verify_otp,name='verify'),
    path('changepass',views.changepassword,name='changepassword'),
    path('empdept',views.employee,name='employee'),
    path('emp/<str:dept>/',views.emp_by_dept,name='dept'),
]