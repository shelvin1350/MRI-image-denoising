from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.files.storage import FileSystemStorage
import MySQLdb
from django.core.files.storage import FileSystemStorage

db = MySQLdb.connect("localhost", "root", "", "mri")
c = db.cursor()


#####common*************************************
def index(request):
    return render(request, "common/index.html")


def patienthome(request):
    return render(request, "patient/index.html")


def login(request):
    msg = ""
    if request.POST:
        uname = request.POST.get("email")
        password = request.POST.get("password")

        request.session['uname'] = uname
        print(uname)
        print(password)
        query = "select * from login where uname='" + uname + "' and password='" + password + "'"
        c.execute(query)
        data = c.fetchone()
        print(data)
        if data:
            if data[2] == 'admin':
                return HttpResponseRedirect("/adminhome/")
            elif data[2] == 'doctor' and data[3] == "approved":
                c.execute("select did from doctorreg where email='" + request.session['uname'] + "'")
                owner = c.fetchone()
                request.session['docid'] = owner[0]
                return HttpResponseRedirect("/doctorhome/")
            elif data[2] == "lab" and data[3] == "approved":
                print("hello")
                a = "select rid from labreg where email='" + str(uname) + "'"
                c.execute(a)
                userid = c.fetchone()
                print(a)
                print(userid)
                request.session['rid'] = userid[0]
                return HttpResponseRedirect("/labhome/")
            elif data[2] == "user" and data[3] == "approved":
                print("hello")
                a = "select pid from patientreg where email='" + str(uname) + "'"
                c.execute(a)
                userid = c.fetchone()
                print(a)
                print(userid)
                request.session['rid'] = userid[0]
                request.session['pid'] = userid[0]
                return HttpResponseRedirect("/userhome/")
        else:
            msg = "invalid username or password"

    return render(request, "common/login.html", {"msg": msg})


################----admin----###########################################
def adminhome(request):
    return render(request, "admin/adminhome.html")
    #####doctor registration####


def adddoctor(request):
    msg = ""
    word = ""
    if request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        phoneno = request.POST.get("phoneno")
        specification = request.POST.get("specification")
        qualification = request.POST.get("qualification")
        qq = "select count(*) from doctorreg where email='" + str(email) + "'"
        c.execute(qq)
        data = c.fetchone()
        print(qq)
        print(data)

        if int(data[0]) < 1:
            query = "insert into doctorreg(name,email,phoneno,specification,qualification) values('" + name + "','" + email + "','" + str(
                phoneno) + "','" + specification + "','" + qualification + "')"
            c.execute(query)
            db.commit()
            usertype = 'doctor'
            status = "approved"

            qqq = "insert into login(uname,password,usertype,status) values('" + email + "','" + phoneno + "','" + usertype + "','" + status + "')"
            c.execute(qqq)
            db.commit()
            msg = "Account successfully Created"
        else:
            msg = "Allready have an account with same mail id"

        # return HttpResponseRedirect("/index/")
    return render(request, "admin/adddoctor.html", {"msg": msg, "word": word})

    ##### lab registration####


def labhome(request):
    return render(request, "lab/labhome.html")


def labreg(request):
    msg = ""
    word = ""
    if request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        phoneno = request.POST.get("phoneno")
        qualification = request.POST.get("qualification")
        status = 'approved'
        qq = "select count(*) from labreg where email='" + str(email) + "'"
        c.execute(qq)
        data = c.fetchone()
        print(qq)
        print(data)

        if int(data[0]) < 1:
            query = "insert into labreg(name,email,phoneno,qualification) values('" + name + "','" + email + "','" + str(
                phoneno) + "','" + qualification + "')"
            c.execute(query)
            db.commit()
            usertype = 'lab'

            qqq = "insert into login(uname,password,usertype,status) values('" + email + "','" + phoneno + "','" + usertype + "','" + status + "')"
            c.execute(qqq)
            db.commit()
            msg = "Account successfully Created"
        else:
            msg = "Allready have an account with same mail id"

        # return HttpResponseRedirect("/index/")
    return render(request, "admin/addlab.html", {"msg": msg, "word": word})


def adminviewdoctors(request):
    c.execute("select * from doctorreg")
    data = c.fetchall()
    return render(request, "admin/adminviewdoctors.html", {"data": data})


def removedoctors(request):
    id = request.GET.get("id")
    xc = "delete  from doctorreg where did='" + str(id) + "'"
    print(xc)
    c.execute(xc)
    db.commit()
    return HttpResponseRedirect("/adminviewdoctors")


def adminchangepassword(request):
    msg = ""
    uname = request.POST.get("email")
    oldpassword = request.POST.get("oldpassword")
    newpassword = request.POST.get("newpassword")
    cpassword = request.POST.get("cpassword")
    print(oldpassword)
    if newpassword == cpassword:
        c.execute("update login set password='" + str(newpassword) + "' where uname='" + str(uname) + "'")
        db.commit()
    return render(request, "admin/changepassword.html", {"msg": msg})


################doctor###########################################
def doctorhome(request):
    return render(request, "doctor/doctorhome.html")


def viewpatientsbydoc(request):

    status = 'booked'
    c.execute(
        "select patientbooking.*,patientreg.* from patientbooking inner join patientreg on patientbooking.pid=patientreg.pid where patientbooking.did='" + str(
            request.session['docid']) + "' and status='" + str(status) + "'")
    data = c.fetchall()
    return render(request, "doctor/viewpatients.html", {"data": data})


def viewmripatients(request):

    status = 'booked'
    # ui = "select patientbooking.*,patientreg.*,mri.* from patientbooking inner join patientreg on patientbooking.pid=patientreg.pid join mri on patientreg.pid=mri.pid where patientbooking.did='" + str(
    #     request.session['docid']) + "' and patientbooking.status='mri'"

    ul="SELECT mri.*,patientreg.* from mri ,patientreg where mri.did='"+str(request.session['docid'])+"' and patientreg.pid=mri.pid"
    print(ul)
    c.execute(ul)
    data = c.fetchall()
    print(data)
    return render(request, "doctor/viewmripatients.html", {"data": data})


def viewmriresult(request):
    id = request.GET.get("id")
    if request.GET.get("id"):
        id = request.GET.get("id")
        print(id)
        ui = "select mri.*,patientreg.* from mri join patientreg on mri.pid=patientreg.pid where mriid='" + str(id) + "'"
        print(ui)
        c.execute(ui)
        data = c.fetchone()
    return render(request, "doctor/viewmriresult.html", {"i": data})


def addprescription(request):
    if request.GET.get("id"):
        pid = request.GET.get("id")
    if request.POST:
        details = request.POST.get("details")
        prescription = request.POST.get("prescription")
        did = request.session['docid']
        qqq = "insert into addprescription(pid,did,details,prescription) values('" + str(pid) + "','" + str(
            did) + "','" + details + "','" + prescription + "')"
        c.execute(qqq)
        db.commit()
        c.execute("update patientbooking set status='completed' where pid='" + str(pid) + "'")
        db.commit()
    return render(request, "doctor/addprescription.html")


def doctorchangepassword(request):
    msg = ""
    uname = request.POST.get("email")
    oldpassword = request.POST.get("oldpassword")
    newpassword = request.POST.get("newpassword")
    cpassword = request.POST.get("cpassword")
    print(oldpassword)
    if newpassword == cpassword:
        c.execute("update login set password='" + str(newpassword) + "' where uname='" + str(uname) + "'")
        db.commit()
    return render(request, "doctor/doctorchangepassword.html")


def addreference(request):
    if request.GET.get("id"):
        pid = request.GET.get("id")
        did = request.session['docid']
        qqq = "insert into mri(pid,did,status) values('" + str(pid) + "','" + str(did) + "','requested')"
        c.execute(qqq)
        db.commit()
        c.execute("update patientbooking set status='mri' where pid='" + str(pid) + "'")
        db.commit()
    return HttpResponseRedirect("/viewpatientsbydoc")


################--lab---###########################################
def selectspecification(request):
    c.execute("select * from doctorreg")
    data = c.fetchall()
    if request.POST:
        specification = request.POST.get("specification")
        request.session['specification'] = specification
        print(specification)
        return HttpResponseRedirect("/patientbooking/")
    return render(request, "patient/selectdoctor.html", {"data": data})


def addpatient(request):
    msg = ""
    if request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        phoneno = request.POST.get("phoneno")

        qqq = "insert into patientreg(name,email,phoneno) values('" + name + "','" + email + "','" + str(phoneno) + "')"
        c.execute(qqq)
        db.commit()

        qqq = "insert into login(uname,password,usertype,status) values('" + email + "','" + phoneno + "','user','approved')"
        c.execute(qqq)
        db.commit()
        c.execute("select * from patientreg where email='" + email + "'")
        data = c.fetchone()
        a = data[0]
        msg = "Patient Registration successfully completed"
    return render(request, "common/addpatient.html", {"msg": msg})


def patientbooking(request):

    msg = ""
    uid=request.session["pid"]
    print(uid,"kuhdiuegdiuegduegydyug")
    c.execute("select * from doctorreg where specification='" + request.session['specification'] + "'")
    data = c.fetchall()
    print(data)
    if request.POST:
        pid = request.POST.get("pid")
        did = request.POST.get("doctor")
        status = 'booked'

        qqq = "insert into patientbooking(pid,did,status) values('" + str(uid) + "','" + str(did) + "','" + str(
            status) + "')"
        c.execute(qqq)
        db.commit()
        c.execute("select count(*) from patientbooking")
        data = c.fetchall()
        a = int(data[0][0]) + 1
        print(type(a))
        msg = "Booking for doctor successfull. Your token number is " 
        msg = msg + str(a)
    return render(request, "patient/patientbooking.html", {"data": data, "msg": msg})


def viewpatients(request):
    status = 'booked'
    c.execute(
        "select patientbooking.*,patientreg.*,doctorreg.* from patientbooking inner join patientreg on patientbooking.pid=patientreg.pid inner join doctorreg on doctorreg.did=patientbooking.did where patientbooking.status='" + str(
            status) + "'")
    data = c.fetchall()
    return render(request, "lab/viewpatients.html", {"data": data})


def viewprescription(request):
    data = ""
    if request.GET.get("id"):
        idd = request.GET.get("id")
        status = 'booked'
        c.execute(
            "select addprescription.*,patientbooking.* from addprescription join patientbooking where addprescription.pid='" + str(
                idd) + "' and patientbooking.status='" + str(status) + "'")
        data = c.fetchone()
        request.session['idd'] = idd

    return render(request, "lab/viewprescription.html", {"data": data})


def removepatient(request):
    msg = ""
    if request.GET.get("id"):
        idd = request.GET.get("id")
        status = 'discharge'
        print(idd)
        print(status)
        c.execute("update patientbooking set status='" + status + "' where pid='" + str(idd) + "'")
        db.commit()
        # c.execute("select patientbooking.*,patientreg.*,doctorreg.* from patientbooking inner join patientreg on patientbooking.pid=patientreg.pid inner join doctorreg on doctorreg.did=patientbooking.did")
        # data=c.fetchall()
        msg = "patient removed"
    return render(request, "lab/viewpatients.html", {"msg": msg})


def labchangepassword(request):
    msg = ""
    if request.POST:
        uname = request.POST.get("email")
        oldpassword = request.POST.get("oldpassword")
        newpassword = request.POST.get("newpassword")
        cpassword = request.POST.get("cpassword")
        print(oldpassword)
        if newpassword == cpassword:
            c.execute("update login set password='" + newpassword + "' where uname='" + uname + "'")
            db.commit()
    return render(request, "lab/labchangepassword.html")


def viewlab(request):
    data = ""

    c.execute("select * from labreg ")
    data = c.fetchall()
    return render(request, "admin/viewlab.html", {"data": data})


def removelab(request):
    id = request.GET.get("id")
    xc = "delete  from labreg where rid='" + str(id) + "'"
    print(xc)
    c.execute(xc)
    db.commit()
    return HttpResponseRedirect("/viewlab")


def adminviewpatients(request):
    data = ""

    c.execute("select * from patientreg ")
    data = c.fetchall()
    return render(request, "admin/viewpatients.html", {"data": data})


def viewmrirequest(request):
    c.execute(
        "select mri.*,patientreg.*,doctorreg.* from mri join patientreg on mri.pid=patientreg.pid join doctorreg on doctorreg.did=mri.did where mri.status='requested'")
    data = c.fetchall()
    print(data)
    return render(request, "lab/viewmri.html", {"data": data})


def uploadimage(request):
    id = request.GET.get("id")
    if request.POST:
        image = request.GET.get("image")
        img = request.FILES["image"]
        fs = FileSystemStorage()
        filename = fs.save(img.name, img)
        url = fs.url(filename)
        c.execute("update mri set image='" + str(url) + "' where mriid='" + str(id) + "'")
        db.commit()
    return render(request, "lab/uploadimage.html")

    ###########ALGORITHM ###########


def clearimage(request):
    id = request.GET.get("image")

    # print(image)
    import imagedenoising
    imagedenoising.denoise(id)
    return HttpResponseRedirect("/viewmripatients")


def profile(request):
    pid=request.session['pid']
    c.execute("select * from patientreg where pid='"+str(pid)+"'")
    data=c.fetchone()
    return render(request,"patient/profile.html",{"data":data})

