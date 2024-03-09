"""clinicmanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clinicapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # common
    path('index/', views.index),
    path('login/', views.login),
    path('', views.index),

  # patient
    path('patienthome/', views.patienthome),
    path('userhome/', views.patienthome),
    path('patientbooking/', views.patientbooking),
    path('profile/', views.profile),
 

    #admin
    path('adminhome/', views.adminhome),
    path('adddoctor/', views.adddoctor),
    path('labreg/', views.labreg),
    path('adminviewdoctors/', views.adminviewdoctors),
    path('adminchangepassword/', views.adminchangepassword),
    path('viewlab/', views.viewlab),
    path('removedoctors/', views.removedoctors),
    path('addlab/', views.labreg),





    #doctor 
    path('doctorhome/', views.doctorhome),
    path('addprescription/', views.addprescription),
    path('viewpatientsbydoc/', views.viewpatientsbydoc),

    path('doctorchangepassword/', views.doctorchangepassword),
    path('addreference/', views.addreference),
    path('viewmripatients/', views.viewmripatients),
    path('viewmriresult/', views.viewmriresult),
    path('clearimage/', views.clearimage),





    #lab
    path('labhome/', views.labhome),
    path('selectspecification/', views.selectspecification),
    path('addpatient/', views.addpatient),
    path('viewpatients/', views.viewpatients),
    path('viewprescription/', views.viewprescription),
   
    path('patientbooking/', views.patientbooking),
    path('labchangepassword/', views.labchangepassword),
  
    path('removepatient/', views.removepatient),
    path('viewmrirequest/', views.viewmrirequest),
    path('uploadimage/', views.uploadimage),




]
