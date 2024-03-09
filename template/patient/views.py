from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.core.files.storage import FileSystemStorage
import MySQLdb
db=MySQLdb.connect("localhost","root","","mri")
c=db.cursor()

#####common*************************************
def index(request):
    return render(request,"common/index.html")


def login(request):
    msg=""
    if request.POST:
        uname=request.POST.get("email")
        password=request.POST.get("password")
       
        request.session['uname']=uname
        print(uname)
        print(password)
        query="select * from login where uname='"+uname+"' and password='"+password+"'"
        c.execute(query)
        data=c.fetchone()
        print(data)
        if data:
            if data[2]=='admin':
                return HttpResponseRedirect("/adminhome/")
            elif data[2]=='doctor' and data[3]=="approved":
                c.execute("select did from doctorreg where email='"+request.session['uname']+"'")
                owner=c.fetchone()
                request.session['docid']=owner[0]
                return HttpResponseRedirect("/doctorhome/")
            elif data[2]=="lab" and data[3]=="approved":
                print("hello")
                a="select rid from labreg where email='"+str(uname)+"'"
                c.execute(a)
                userid=c.fetchone()
                print(a)
                print(userid)
                request.session['rid']=userid[0]
                return HttpResponseRedirect("/labhome/")
            elif data[2]=="user" and data[3]=="approved":
                print("hello")
                a="select pid from patientreg where email='"+str(uname)+"'"
                c.execute(a)
                userid=c.fetchone()
                print(a)
                print(userid)
                request.session['rid']=userid[0]
                request.session['pid']=userid[0]
                return HttpResponseRedirect("/userhome/")
        else:
            msg="invalid username or password"
           


    return render(request,"common/login.html",{"msg":msg})





################----admin----###########################################
def adminhome(request):
    return render(request,"admin/adminhome.html")
            #####doctor registration####
def adddoctor(request):
    

    msg=""
    word=""
    if request.POST:
        name=request.POST.get("name")
        email=request.POST.get("email")
        phoneno=request.POST.get("phoneno")
        specification=request.POST.get("specification")
        qualification=request.POST.get("qualification")
        qq="select count(*) from doctorreg where email='"+str(email)+"'"
        c.execute(qq)
        data=c.fetchone()
        print(qq)
        print(data)
 
        if int(data[0])<1:
            query="insert into doctorreg(name,email,phoneno,specification,qualification) values('"+ name +"','"+ email +"','"+str(phoneno)+"','"+ specification +"','"+ qualification +"')"
            c.execute(query)
            db.commit()
            usertype='doctor'
            status="approved"

            qqq="insert into login(uname,password,usertype,status) values('"+ email +"','"+phoneno+"','"+usertype+"','"+status+"')"
            c.execute(qqq)
            db.commit()
            msg="Account successfully Created"
        else:
            msg="Allready have an account with same mail id"


        # return HttpResponseRedirect("/index/")
    return render(request,"admin/adddoctor.html",{"msg":msg,"word":word})



            ##### lab registration####
def labhome(request):
    return render(request,"lab/labhome.html")
def labreg(request):
    msg=""
    word=""
    if request.POST:
        name=request.POST.get("name")
        email=request.POST.get("email")
        phoneno=request.POST.get("phoneno")
        qualification=request.POST.get("qualification")
        status='approved'
        qq="select count(*) from labreg where email='"+str(email)+"'"
        c.execute(qq)
        data=c.fetchone()
        print(qq)
        print(data)
 
        if int(data[0])<1:
            query="insert into labreg(name,email,phoneno,qualification) values('"+ name +"','"+ email +"','"+str(phoneno)+"','"+ qualification +"')"
            c.execute(query)
            db.commit()
            usertype='lab'

            qqq="insert into login(uname,password,usertype,status) values('"+ email +"','"+phoneno+"','"+usertype+"','"+status+"')"
            c.execute(qqq)
            db.commit()
            msg="Account successfully Created"
        else:
            msg="Allready have an account with same mail id"


        # return HttpResponseRedirect("/index/")
    return render(request,"admin/addlab.html",{"msg":msg,"word":word})


def adminviewdoctors(request):
    c.execute("select * from doctorreg")
    data=c.fetchall()
    return render(request,"admin/adminviewdoctors.html",{"data":data})

def removedoctors(request):
    id=request.GET.get("id")
    xc="delete  from doctorreg where did='"+str(id)+"'"
    print(xc)
    c.execute(xc)
    db.commit()
    return HttpResponseRedirect("/adminviewdoctors")



def adminchangepassword(request):
    msg=""
    uname=request.POST.get("email")
    oldpassword=request.POST.get("oldpassword")
    newpassword=request.POST.get("newpassword")
    cpassword=request.POST.get("cpassword")
    print(oldpassword)
    if newpassword==cpassword:
        c.execute("update login set password='"+str(newpassword)+"' where uname='"+str(uname)+"'")
        db.commit()
    return render(request,"admin/changepassword.html",{"msg":msg})
    

################doctor###########################################
def doctorhome(request):
    return render(request,"doctor/doctorhome.html")

def viewpatientsbydoc(request):
    status='booked'
    c.execute("select patientbooking.*,patientreg.* from patientbooking inner join patientreg on patientbooking.pid=patientreg.pid where patientbooking.did='"+str(request.session['docid'])+"' and status='"+str(status)+"'")
    data=c.fetchall()
    return render(request,"doctor/viewpatients.html",{"data":data})

def addprescription(request):
    if request.GET.get("id"):
        pid=request.GET.get("id")
    if request.POST:
        details=request.POST.get("details")
        prescription=request.POST.get("prescription")
        did=request.session['docid']
        qqq="insert into addprescription(pid,did,details,prescription) values('"+ str(pid) +"','"+str(did)+"','"+details+"','"+prescription+"')"
        c.execute(qqq)
        db.commit()
    return render(request,"doctor/addprescription.html")


def doctorchangepassword(request):
    msg=""
    uname=request.POST.get("email")
    oldpassword=request.POST.get("oldpassword")
    newpassword=request.POST.get("newpassword")
    cpassword=request.POST.get("cpassword")
    print(oldpassword)
    if newpassword==cpassword:
        c.execute("update login set password='"+str(newpassword)+"' where uname='"+str(uname)+"'")
        db.commit()
    return render(request,"doctor/doctorchangepassword.html")
        





################--lab---###########################################
def selectspecification(request):
    c.execute("select * from doctorreg")
    data=c.fetchall()
    if request.POST:
        specification=request.POST.get("specification")
        request.session['specification']=specification
        print(specification)
        return HttpResponseRedirect("/patientbooking/")
    return render(request,"lab/selectdoctor.html",{"data":data})


def addpatient(request):
    msg=""
    if request.POST:
        name=request.POST.get("name")
        email=request.POST.get("email")
        phoneno=request.POST.get("phoneno")
       
        qqq="insert into patientreg(name,email,phoneno) values('"+ name +"','"+ email +"','"+str(phoneno)+"')"
        c.execute(qqq)
        db.commit()
        
        qqq="insert into login(uname,password,usertype,status) values('"+ email +"','"+phoneno+"','user','approved')"
        c.execute(qqq)
        db.commit()
        c.execute("select * from patientreg where email='"+ email +"'")
        data=c.fetchone()
        a=data[0]
        msg=a
    return render(request,"common/addpatient.html",{"msg":msg})


def patientbooking(request):
    msg=""
    c.execute("select * from doctorreg where specification='"+request.session['specification']+"'")
    data=c.fetchall()
    print(data)
    if request.POST:
        pid=request.POST.get("pid")
        did=request.POST.get("doctor")
        status='booked'
    
       
        qqq="insert into patientbooking(pid,did,status) values('"+str(pid) +"','"+ str(did) +"','"+ str(status) +"')"
        c.execute(qqq)
        db.commit()
        c.execute("select count(*) from patientbooking")
        data=c.fetchall()
        a=int(data[0][0])+1
        print(type(a))
        msg=a
    return render(request,"lab/patientbooking.html",{"data":data,"msg":msg})
        
def viewpatients(request):
    status='booked'
    c.execute("select patientbooking.*,patientreg.*,doctorreg.* from patientbooking inner join patientreg on patientbooking.pid=patientreg.pid inner join doctorreg on doctorreg.did=patientbooking.did where patientbooking.status='"+str(status)+"'")
    data=c.fetchall()
    return render(request,"lab/viewpatients.html",{"data":data})

def viewprescription(request):
    data=""
    if request.GET.get("id"):
        idd=request.GET.get("id")
        status='booked'
        c.execute("select addprescription.*,patientbooking.* from addprescription join patientbooking where addprescription.pid='"+str(idd)+"' and patientbooking.status='"+str(status)+"'")
        data=c.fetchone()
        request.session['idd']=idd
        
    return render(request,"lab/viewprescription.html",{"data":data})

def admit(request):
    if request.GET.get("id"):
        idd=request.GET.get("id")
        status='admit'
        print(idd)
        print(status)
        c.execute("update patientbooking set status='"+status+"' where pid='"+str(idd)+"'")
        db.commit()
        # c.execute("select patientbooking.*,patientreg.*,doctorreg.* from patientbooking inner join patientreg on patientbooking.pid=patientreg.pid inner join doctorreg on doctorreg.did=patientbooking.did")
        # data=c.fetchall()
        msg="patient admitted"
    return render(request,"lab/viewpatients.html",{"msg":msg})

def removepatient(request):
    msg=""
    if request.GET.get("id"):
        idd=request.GET.get("id")
        status='discharge'
        print(idd)
        print(status)
        c.execute("update patientbooking set status='"+status+"' where pid='"+str(idd)+"'")
        db.commit()
        # c.execute("select patientbooking.*,patientreg.*,doctorreg.* from patientbooking inner join patientreg on patientbooking.pid=patientreg.pid inner join doctorreg on doctorreg.did=patientbooking.did")
        # data=c.fetchall()
        msg="patient removed"
    return render(request,"lab/viewpatients.html",{"msg":msg})


def viewdischarge(request):
    status='admit'
    c.execute("select  patientbooking.*,patientreg.* from patientbooking join patientreg on  patientbooking.pid=patientreg.pid where patientbooking.status='"+status+"'")
    data=c.fetchall()
    return render(request,"lab/viewadmittedpatients.html",{"data":data})

def discharge(request):
    if request.GET.get("id"):
        idd=request.GET.get("id")
        status='discharge'
        c.execute("update patientbooking set status='"+status+"' where pid='"+str(idd)+"'")
        db.commit()
        return HttpResponseRedirect("/viewdischarge/")
    return render(request,"lab/viewadmittedpatients.html")



def labchangepassword(request):
    msg=""
    if request.POST:
        uname=request.POST.get("email")
        oldpassword=request.POST.get("oldpassword")
        newpassword=request.POST.get("newpassword")
        cpassword=request.POST.get("cpassword")
        print(oldpassword)
        if newpassword==cpassword:
            c.execute("update login set password='"+newpassword+"' where uname='"+uname+"'")
            db.commit()
    return render(request,"lab/labchangepassword.html")
        

def createbill(request):
    total=""
    if request.POST:
        considerationbill=request.POST.get("considerationbill")
        medicinebill=request.POST.get("medicinebill")
        othercharges=request.POST.get("othercharges")
        total=int(othercharges)+int(medicinebill)+int(considerationbill)
        # return HttpResponse("total amount='"+str(total)+"'")
        request.session["cbill"]=considerationbill
        request.session["mbill"]=medicinebill
        request.session["obill"]=othercharges
        request.session["total"]=total
        return render(request,"lab/viewbill.html",{"cbill":considerationbill,"mbill":medicinebill,"obill":othercharges,"total":total})

    return render(request,"lab/createbill.html",{"msg":total})




def viewlab(request):
    data=""
    
    c.execute("select * from labreg ")
    data=c.fetchall()
    return render(request,"admin/viewlab.html",{"data":data})


def removelab(request):
    id=request.GET.get("id")
    xc="delete  from labreg where rid='"+str(id)+"'"
    print(xc)
    c.execute(xc)
    db.commit()
    return HttpResponseRedirect("/viewlab")


def adminviewpatients(request):
    data=""
    
    c.execute("select * from patientreg ")
    data=c.fetchall()
    return render(request,"admin/viewpatients.html",{"data":data})