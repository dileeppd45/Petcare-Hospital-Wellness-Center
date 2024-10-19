from django.shortcuts import render

from django.shortcuts import render, HttpResponse, redirect
from django.db import connection
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

import os
# reg.text

def home_page(request):
	return render(request, 'index.html')

def login(request):
	if request.method == "POST":
		userid = request.POST['name']
		password = request.POST['password']
		cursor = connection.cursor()
		cursor.execute("select * from login where admin_id= '" + userid + "' AND password = '" + password + "'")
		admin = cursor.fetchone()
		if admin == None:
			cursor.execute("select * from common_staff where reg_no='"+userid+"' and password='"+password+"'")
			staff = cursor.fetchone()
			if staff ==None:
				cursor.execute("select * from user_register where user_id='"+userid+"' and password='"+password+"'")
				user = cursor.fetchone()
				if user==None:
					cursor.execute("select * from doctor where reg_no ='"+userid+"' and password ='"+password+"'")
					doctor = cursor.fetchone()
					if doctor == None:
						return HttpResponse("<script> alert('Invalid Username Or Password!!');window.location='../login';</script>")
					else:
						print(doctor)
						request.session['doctorid']=userid
						return HttpResponse("<script> alert('welcome doctor "+doctor[1]+"');window.location='../doctor_home';</script>")					
				else:
					request.session['uid']=userid
					return HttpResponse("<script> alert('welcome "+user[1]+"');window.location='../user_home';</script>")
			else:
				request.session['staffid']=userid
				return HttpResponse("<script> alert('welcome Pharmasy Staff "+staff[1]+"');window.location='../staff_home';</script>")
		else:
			request.session['adminid']=userid
			return HttpResponse("<script> alert('welcome Admin');window.location='../admin_home';</script>")	   
	return render(request, "login.html")

def register(request):
	if request.method == 'POST':
		userid = request.POST['userid']
		name = request.POST['name']
		address = request.POST['address']
		phone = request.POST['phone']
		email = request.POST['email']
		password = request.POST['password']
		cursor = connection.cursor()
		cursor.execute("select * from user_register where user_id='"+userid+"' ")
		data = cursor.fetchone()
		if data ==None:
			cursor.execute("select * from login where admin_id ='"+userid+"'")
			data = cursor.fetchone()
			if data == None:
				cursor.execute("select * from doctor where reg_no ='"+userid+"'")
				data = cursor.fetchone()
				if data == None:
					cursor.execute("select * from common_staff where reg_no='"+userid+"'")
					data = cursor.fetchone()
					if data == None:
						cursor.execute("insert into user_register values('"+userid+"','"+name+"','"+address+"','"+phone+"','"+email+"','"+password+"')")
						request.session['uid'] = userid
						return HttpResponse("<script>alert('welcome " +name+ " ');window.location='../user_home';</script>")
		else:
			return HttpResponse("<script>alert('userid already registered please add unique userid');window.location='../register';</script>")
	return render(request,'register.html')


    



#admin

def admin_home(request):

    return render(request,'admin/index1.html')

def reg_category(request):
	return render(request, "admin/admin_reg_dep.html")

def add_category(request):
	if request.method == "POST":
		name = request.POST['name']
		details = request.POST['details']
		cursor = connection.cursor()
		cursor.execute("insert into category values(null,'" + name + "','" + details + "')")
		cursor.close()
		connection.close()
		cursor.close()
		connection.close()
		return redirect("view_category")
def view_category(request):
	cursor = connection.cursor()
	cursor.execute("select * from category")
	data=cursor.fetchall()
	cursor.close()
	connection.close()
	return render(request,"admin/admin_view_department.html",{'cdata':data})

def reg_staff(request):

	return render(request,"admin/admin_reg_staff.html")
def add_staff(request):
	if request.method == "POST":
		name = request.POST['name']
		staff_type= request.POST['staff_type']
		address =request.POST['address']
		phone = request.POST['phone']
		email = request.POST['email']
		password = request.POST['txtpassword']
		experience = request.POST['experience']
		cursor = connection.cursor()
		if staff_type == "doctor":
			cursor.execute("insert into doctor values(null,'"+str(name)+"','"+str(address)+"','"+str(phone)+"','"+str(email)+"','"+str(password)+"','" + str(experience) + "','not_set','available') ")
			last_id = cursor.lastrowid
			reg_no = "PETCARED" + str(last_id)
			print(reg_no, "reg_no")
			cursor.execute("update doctor set reg_no='"+reg_no+"' where doctor_id='"+str(last_id)+"' ")
		elif staff_type =="staff":
			cursor.execute("insert into common_staff values(null,'"+str(name)+"','"+str(address)+"','"+str(phone)+"','"+str(email)+"','"+str(password)+"','" + str(experience) + "','not_set','available') ")
			last_id = cursor.lastrowid
			reg_no = "PETCARES"+str(last_id)
			print(reg_no,"reg_no")
			cursor.execute("update common_staff set reg_no='"+reg_no+"' where staff_id='"+str(last_id)+"' ")
		cursor.close()
		connection.close()
		return redirect("view_staff")

def view_staff(request):
	cursor = connection.cursor()
	cursor.execute("select * from doctor where leave_status = 'available' or leave_status ='not available' ")
	ddata=cursor.fetchall()
	cursor.execute("select * from common_staff  where leave_status = 'available' or leave_status ='not available' ")
	sdata = cursor.fetchall()
	cursor.close()
	connection.close()
	return render(request,"admin/admin_view_staff.html",{'ddata':ddata,'sdata':sdata})

def edit_staff(request,id):
	cursor = connection.cursor()
	if request.method == "POST":
		name = request.POST['name']
		address =request.POST['address']
		phone = request.POST['phone']
		email = request.POST['email']
		password = request.POST['txtpassword']
		experience = request.POST['experience']
		cursor.execute("update common_staff set name='"+name+"' where staff_id='"+id+"'")
		cursor.execute("update common_staff set address='"+address+"' where staff_id='"+id+"'")
		cursor.execute("update common_staff set phone='"+phone+"' where staff_id='"+id+"'")
		cursor.execute("update common_staff set email='"+email+"' where staff_id='"+id+"'")
		cursor.execute("update common_staff set password='"+password+"' where staff_id='"+id+"'")
		cursor.execute("update common_staff set experience='"+experience+"' where staff_id='"+id+"'")
		return HttpResponse("<script>alert('Updated'); window.location='../view_staff';</script>")

	cursor.execute("select * from common_staff where staff_id ='"+str(id)+"'")
	doctor = cursor.fetchone()
	return render(request,'admin/edit_staff.html',{'doctor':doctor})

def edit_dstaff(request,id):
	cursor = connection.cursor()
	if request.method == "POST":
		name = request.POST['name']
		address =request.POST['address']
		phone = request.POST['phone']
		email = request.POST['email']
		password = request.POST['txtpassword']
		experience = request.POST['experience']
		cursor.execute("update doctor set name='"+name+"' where doctor_id='"+id+"'")
		cursor.execute("update doctor set address='"+address+"' where doctor_id='"+id+"'")
		cursor.execute("update doctor set phone='"+phone+"' where doctor_id='"+id+"'")
		cursor.execute("update doctor set email='"+email+"' where doctor_id='"+id+"'")
		cursor.execute("update doctor set password='"+password+"' where doctor_id='"+id+"'")
		cursor.execute("update doctor set experience='"+experience+"' where doctor_id='"+id+"'")
		return HttpResponse("<script>alert('Updated'); window.location='../view_staff';</script>")

	cursor.execute("select * from doctor where doctor_id ='"+str(id)+"'")
	doctor = cursor.fetchone()
	return render(request,'admin/edit_doctor.html',{'doctor':doctor})
def remove_dstaff(request,id):
	cursor = connection.cursor()
	cursor.execute("select * from consultation where doctorid='"+id+"' and status='active'")
	data = cursor.fetchone()
	if data is not None:
		return HttpResponse("<script>alert('there is still active consultations so cannot remove him now'); window.location='../view_staff';</script>")
	cursor.execute("select * from doctor where leave_status ='available' or leave_status ='not available'")
	data = cursor.fetchone()
	if data == None:
		return HttpResponse("<script>alert('there is no more doctors so now you cant remove '); window.location='../view_staff';</script>")
	cursor.execute("update doctor set leave_status ='removed' where doctor_id='"+id+"'")
	return HttpResponse("<script>alert('removed'); window.location='../view_staff';</script>")
def remove_staff(request,id):
	cursor = connection.cursor()

	cursor.execute("select * from common_staff where leave_status ='available' or leave_status ='not available'")
	data = cursor.fetchone()
	if data == None:
		return HttpResponse("<script>alert('there is no more Staffs so now you cant remove'); window.location='../view_staff';</script>")
	cursor.execute("select * from medicine_prescription where staff_id='"+id+"' and status='requested' or staff_id='"+id+"' and status='approved' ")
	request = cursor.fetchone()	
	if request is not None:
		cursor.execute("select * from medicine_prescription where staff_id='"+id+"' and status='requested' or staff_id='"+id+"' and status='approved' ")
		req = cursor.fetchall()
		for i in req:
			cursor.execute("update medicine_prescription set staff_id ='"+str(data[0])+"' where medicine_prescription_id ='"+str(i[0])+"'")
	cursor.execute("select * from medicine_prescription as m join prescription_bill as p where m.staff_id='"+id+"' and m.status ='approved'  and m.medicine_prescription_id = p.medicine_prescription_id and p.status ='processing'")
	pata = cursor.fetchone()
	if pata is not None:
		cursor.execute("select * from medicine_prescription as m join prescription_bill as p where m.staff_id='"+id+"' and m.status ='approved'  and m.medicine_prescription_id = p.medicine_prescription_id and p.status ='processing'")
		pd = cursor.fetchall()
		for i in pd:
			cursor.execute("update medicine_prescription set staff_id ='"+str(data[0])+"' where medicine_prescription_id ='"+str(i[0])+"'")
	cursor.execute("update common_staff set leave_status ='removed' where staff_id='"+id+"'")
	return HttpResponse("<script>alert('removed'); window.location='../view_staff';</script>")

def view_doctor_consultations(request,id):
	cursor = connection.cursor()
	request.session['adminviewdoctor']=id
	cursor.execute("select consultation.*,doctor.*,category.name from consultation join doctor join category  where consultation.id_category = category.category_id and consultation.doctorid = doctor.doctor_id and  consultation.status ='active' and consultation.doctorid = '"+str(id)+"'")
	adata = cursor.fetchall()
	sdata=[]
	for i in adata:
		j=[]
		cursor.execute("select * from enquiry_details where consult_id='"+str(i[0])+"' and status ='requested'")
		requenquiry=cursor.fetchone()
		if requenquiry is not None:
			j.append(i[0])
			j.append(i[1])
			j.append(i[2])
			j.append(i[3])
			j.append(i[4])
			j.append(i[5])
			j.append(i[6])
			j.append(i[7])
			j.append(i[8])
			j.append(i[9])
			j.append(i[10])
			j.append(i[11])
			j.append(i[12])
			j.append(i[13])
			j.append(i[14])
			j.append(i[15])
			j.append(i[16])
			j.append("admin_view_user_enquiry")
			j.append("view")

			j=tuple(j)
			sdata.append(j)
	sdata = tuple(sdata)

	print(sdata)
	cursor.execute("select consultation.*,doctor.*,category.name from consultation join doctor join category  where consultation.id_category = category.category_id and consultation.doctorid = doctor.doctor_id and  consultation.status ='complete' and consultation.doctorid = '"+str(id)+"'")
	bdata = cursor.fetchall()
	cdata=[]
	for i in bdata:
		j=[]

		cursor.execute("select * from enquiry_details where consult_id='"+str(i[0])+"' and status='home_remedy'")
		home_remedy =cursor.fetchone()
		if home_remedy is not None:
			j.append(i[0])
			j.append(i[1])
			j.append(i[2])
			j.append(i[3])
			j.append(i[4])
			j.append(i[5])
			j.append(i[6])
			j.append(i[7])
			j.append(i[8])
			j.append(i[9])
			j.append(i[10])
			j.append(i[11])
			j.append(i[12])
			j.append(i[13])
			j.append(i[14])
			j.append(i[15])
			j.append(i[16])
			j.append("admin_view_home_remedies")
			j.append("Home Remedies")

		cursor.execute("select * from enquiry_details where consult_id='"+str(i[0])+"' and status='medicine_prescription'")
		medicine_pres=cursor.fetchone()
		if medicine_pres is not None:
			j.append(i[0])
			j.append(i[1])
			j.append(i[2])
			j.append(i[3])
			j.append(i[4])
			j.append(i[5])
			j.append(i[6])
			j.append(i[7])
			j.append(i[8])
			j.append(i[9])
			j.append(i[10])
			j.append(i[11])
			j.append(i[12])
			j.append(i[13])
			j.append(i[14])
			j.append(i[15])
			j.append(i[16])
			j.append("admin_view_medicine_prescription")
			j.append("Medicine Prescription")

		
		j=tuple(j)
		cdata.append(j)
	cdata = tuple(cdata)



	return render(request,'admin/consultations.html',{'adata':sdata,'bdata':cdata})


def admin_view_medicine_prescription(request,id):
	cursor = connection.cursor()
	did = request.session['adminviewdoctor']
	cursor.execute("select enquiry_details.*,doctor.*,category.name, m.* from enquiry_details join doctor join category join medicine_prescription as m where enquiry_details.consult_id='"+str(id)+"' and enquiry_details.category_id = category.category_id and enquiry_details.doctor_id = doctor.doctor_id and enquiry_details.doctor_id='"+str(did)+"'and enquiry_details.enquiry_details_id = m.enquiry_details_id ")
	adata = cursor.fetchone()
	print(adata)
	cursor.execute("select * from category where category_id='"+str(adata[6])+"'")
	cat = cursor.fetchone()

	return render(request,'admin/view_med_prescription.html',{'adata':adata,'cat':cat})


def admin_view_home_remedies(request,id):
	cursor = connection.cursor()
	did = request.session['adminviewdoctor']
	cursor.execute("select enquiry_details.*,doctor.*,category.name, m.* from enquiry_details join doctor join category join home_remedies as m where enquiry_details.consult_id='"+str(id)+"' and enquiry_details.category_id = category.category_id and enquiry_details.doctor_id = doctor.doctor_id and enquiry_details.doctor_id='"+str(did)+"'and enquiry_details.enquiry_details_id = m.enquiry_details_id ")
	adata = cursor.fetchone()
	print(adata)
	cursor.execute("select * from category where category_id='"+str(adata[6])+"'")
	cat = cursor.fetchone()

	return render(request,'admin/view_home_remedies.html',{'adata':adata,'cat':cat})	



def admin_view_user_enquiry(request,id):
	cursor = connection.cursor()
	did = request.session['adminviewdoctor']
	cursor.execute("select enquiry_details.*,doctor.*,category.name from enquiry_details join doctor join category where enquiry_details.consult_id='"+str(id)+"' and enquiry_details.category_id = category.category_id and enquiry_details.doctor_id = doctor.doctor_id and enquiry_details.doctor_id='"+str(did)+"' ")
	adata = cursor.fetchone()
	cursor.execute("select * from category where category_id='"+str(adata[6])+"'")
	cat = cursor.fetchone()

	return render(request,'admin/enquiry_not_replied.html',{'adata':adata,'cat':cat})


def admin_view_bill(request,id):
	cursor = connection.cursor()
	cursor.execute("select * from medicine_prescription where enquiry_details_id='"+str(id)+"' and status ='not set'")
	data = cursor.fetchone()
	if data is not None:
		cursor.execute("select * from enquiry_details where enquiry_details_id='"+str(id)+"'")
		enq= cursor.fetchone()
		consultid= str(enq[1])
		return HttpResponse("<script>alert('Not Yet Billed'); window.location='../admin_view_medicine_prescription/%s';</script>" % consultid)
	cursor.execute("select * from medicine_prescription where enquiry_details_id='"+str(id)+"' and status ='requested'")
	data = cursor.fetchone()
	if data is not None:
		cursor.execute("select * from enquiry_details where enquiry_details_id='"+str(id)+"'")
		enq= cursor.fetchone()
		consultid= str(enq[1])
		return HttpResponse("<script>alert('Not Yet Billed'); window.location='../admin_view_medicine_prescription/%s';</script>" % consultid)
	cursor.execute("select * from medicine_prescription as m join enquiry_details as e join doctor as d join category as c join common_staff as co where co.staff_id = m.staff_id and m.enquiry_details_id='"+str(id)+"' and m.status ='approved' and m.enquiry_details_id = e.enquiry_details_id and e.doctor_id = d.doctor_id and e.category_id = c.category_id")
	data = cursor.fetchone()
	print(data)
	if data is not None:
		cursor.execute("select * from prescription_bill where medicine_prescription_id='"+str(data[0])+"'")
		presbill = cursor.fetchone()
		total=float(presbill[2])+float(presbill[3])
		return render(request,'admin/payment_for_medicine_bill.html',{'data':data,'total':total,'bill':presbill})
	cursor.execute("select * from medicine_prescription as m join enquiry_details as e join doctor as d join category as c join common_staff as co where co.staff_id = m.staff_id and m.enquiry_details_id='"+str(id)+"' and m.status ='paid' and m.enquiry_details_id = e.enquiry_details_id and e.doctor_id = d.doctor_id and e.category_id = c.category_id")	
	data = cursor.fetchone()
	print(data)
	if data is not None:
		cursor.execute("select * from prescription_bill where medicine_prescription_id='"+str(data[0])+"'")
		presbill = cursor.fetchone()
		total=float(presbill[2])+float(presbill[3])

		return render(request,'admin/view_medicine_bill.html',{'data':data,'total':total,'bill':presbill})

def bill_history(request):
	cursor = connection.cursor()
	cursor.execute("select * from medicine_prescription as m join enquiry_details as e join doctor as d join category as c join prescription_bill as p join common_staff as co where co.staff_id=m.staff_id and  m.status = 'paid' and m.enquiry_details_id = e.enquiry_details_id and e.doctor_id= d.doctor_id and e.category_id= c.category_id  and m.medicine_prescription_id = p.medicine_prescription_id and p.status='Shipped' or m.status = 'paid' and  m.enquiry_details_id = e.enquiry_details_id and e.doctor_id= d.doctor_id and e.category_id= c.category_id  and m.medicine_prescription_id = p.medicine_prescription_id and p.status='Processing' ")
	data =cursor.fetchall()
	sata = []
	t = 0
	for i in data:
		s=list(i)
		billamount=i[32]
		shipcharge=i[33]
		s.append(billamount)
		s.append(shipcharge)
		total=float(billamount)+float(shipcharge)
		t =t +total
		s.append(str(total))
		sata.append(s)	
	sata = tuple(sata)
	print(sata)
	cursor.execute("select * from consultation")
	con = cursor.fetchall()
	cons=0
	count=0
	for i in con:
		cons = cons+float(i[5])
		count = count+1
	total =t +cons
	return render(request,'admin/bill_history.html',{'data':sata,'total':t,'ta':total,'count':count})

def view_users(request):
	cursor = connection.cursor()
	if request.method=='POST':
		user= request.POST['user']
		cursor.execute("select * from user_register where user_id='"+user+"'")
		data = cursor.fetchall()
		return render(request,'admin/view_users.html',{'data':data})
	cursor.execute("select * from user_register")
	data = cursor.fetchall()
	return render(request,'admin/view_users.html',{'data':data})
def admin_view_consultations(request,id):
	request.session['adminuserid']=id
	cursor = connection.cursor()
	cursor.execute("select consultation.*,doctor.*,category.name from consultation join doctor join category  where consultation.id_category = category.category_id and consultation.doctorid = doctor.doctor_id and consultation.user_id='"+str(id)+"' and consultation.status ='active'")
	adata = cursor.fetchall()
	sdata=[]
	for i in adata:
		j=[]
		cursor.execute("select * from enquiry_details where consult_id = '"+str(i[0])+"'")
		noenquiry=cursor.fetchone()
		if noenquiry ==None:
			j.append(i[0])
			j.append(i[1])
			j.append(i[2])
			j.append(i[3])
			j.append(i[4])
			j.append(i[5])
			j.append(i[6])
			j.append(i[7])
			j.append(i[8])
			j.append(i[9])
			j.append(i[10])
			j.append(i[11])
			j.append(i[12])
			j.append(i[13])
			j.append(i[14])
			j.append(i[15])
			j.append(i[16])
			j.append("admin_view_consultations")
			j.append("enquiry not added yet")
			j.append(id)
			j.append("white")
		cursor.execute("select * from enquiry_details where consult_id='"+str(i[0])+"' and status ='requested'")
		requenquiry=cursor.fetchone()
		if requenquiry is not None:
			j.append(i[0])
			j.append(i[1])
			j.append(i[2])
			j.append(i[3])
			j.append(i[4])
			j.append(i[5])
			j.append(i[6])
			j.append(i[7])
			j.append(i[8])
			j.append(i[9])
			j.append(i[10])
			j.append(i[11])
			j.append(i[12])
			j.append(i[13])
			j.append(i[14])
			j.append(i[15])
			j.append(i[16])
			j.append("view_enquiry_not_replied")
			j.append("view enquiry")
			j.append(i[0])

		j=tuple(j)
		sdata.append(j)
	sdata = tuple(sdata)
	
	print(sdata)


	cursor = connection.cursor()
	cursor.execute("select consultation.*,doctor.*,category.name from consultation join doctor join category  where consultation.id_category = category.category_id and consultation.doctorid = doctor.doctor_id and consultation.user_id='"+str(id)+"' and consultation.status ='complete'")
	bdata = cursor.fetchall()
	cdata=[]
	for i in bdata:
		j=[]

		cursor.execute("select * from enquiry_details where consult_id='"+str(i[0])+"' and status='home_remedy'")
		home_remedy =cursor.fetchone()
		if home_remedy is not None:
			j.append(i[0])
			j.append(i[1])
			j.append(i[2])
			j.append(i[3])
			j.append(i[4])
			j.append(i[5])
			j.append(i[6])
			j.append(i[7])
			j.append(i[8])
			j.append(i[9])
			j.append(i[10])
			j.append(i[11])
			j.append(i[12])
			j.append(i[13])
			j.append(i[14])
			j.append(i[15])
			j.append(i[16])
			j.append("admin_view_home_remedies")
			j.append("Home Remedies")

		cursor.execute("select * from enquiry_details where consult_id='"+str(i[0])+"' and status='medicine_prescription'")
		medicine_pres=cursor.fetchone()
		if medicine_pres is not None:
			j.append(i[0])
			j.append(i[1])
			j.append(i[2])
			j.append(i[3])
			j.append(i[4])
			j.append(i[5])
			j.append(i[6])
			j.append(i[7])
			j.append(i[8])
			j.append(i[9])
			j.append(i[10])
			j.append(i[11])
			j.append(i[12])
			j.append(i[13])
			j.append(i[14])
			j.append(i[15])
			j.append(i[16])
			j.append("admin_view_medicine_prescription")
			j.append("Medicine Prescription")

		
		j=tuple(j)
		cdata.append(j)
	cdata = tuple(cdata)
	return render(request,'admin/consultation.html',{'adata':sdata,'bdata':cdata})	
def view_enquiry_not_replied(request,id):
	uid=request.session['adminuserid']
	update_status=""
	cursor=connection.cursor()
	cursor.execute("select enquiry_details.*,doctor.*,category.name from enquiry_details join doctor join category  where enquiry_details.consult_id='"+str(id)+"' and enquiry_details.category_id = category.category_id and enquiry_details.doctor_id= doctor.doctor_id and enquiry_details.user_id='"+str(uid)+"' and enquiry_details.status ='requested'")
	adata = cursor.fetchone()
	cursor.execute("select * from category where category_id='"+str(adata[6])+"'")
	cat = cursor.fetchone()
	cursor.execute("select * from doctor where doctor_id='"+str(adata[7])+"'")
	update_status=""
	doctor = cursor.fetchone()
	if request.method == "POST":
		description= request.POST['description']
		cursor.execute("update enquiry_details set detail_description='"+description+"' where enquiry_details_id='"+str(adata[0])+"'")
		update_status="updated"
	print(adata)
	cursor.execute("select enquiry_details.*,doctor.*,category.name from enquiry_details join doctor join category  where enquiry_details.consult_id='"+str(id)+"' and enquiry_details.category_id = category.category_id and enquiry_details.doctor_id= doctor.doctor_id and enquiry_details.user_id='"+str(uid)+"' and enquiry_details.status ='requested'")
	adata = cursor.fetchone()
	cursor.execute("select * from category where category_id='"+str(adata[6])+"'")
	cat = cursor.fetchone()
	cursor.execute("select * from doctor where doctor_id='"+str(adata[7])+"'")
	
	return render(request,'admin/enquiry_not_repliedu.html',{'adata':adata,'cat':cat,'doctor':doctor,'us':update_status})	



def admin_logout(request):
    return render(request,'admin/LogOut.html')

def doctor_home(request):
	cursor = connection.cursor()
	cursor.execute("select * from doctor where reg_no='"+str(request.session['doctorid'])+"'")
	doctor = cursor.fetchone()
	leave_status=doctor[8]
	if leave_status =='available':
		status='available'
		scol='greenyellow'
	elif leave_status=='not available':
		status ='Not Available'
		scol='red'

	return render(request,'doctor/index1.html',{'status':status,'scol':scol})


def avail_or_not(request):
	cursor = connection.cursor()
	if request.method=='POST':
		stat = request.POST['status']
		if stat=='available':
			cursor.execute("update doctor set leave_status ='not available' where reg_no='"+str(request.session['doctorid'])+"'")
		elif stat=='not available':
			cursor.execute("update doctor set leave_status='available' where reg_no='"+str(request.session['doctorid'])+"'")
	cursor.execute("select * from doctor where reg_no='"+str(request.session['doctorid'])+"'")
	doctor = cursor.fetchone()
	leave_status=doctor[8]
	if leave_status =='available':
		status='available'
		scol='greenyellow'
	elif leave_status=='not available':
		status ='not available'
		scol='red'
		
	return render(request,'doctor/avail_or_not.html',{'status':status,'scol':scol})

def view_consultation(request):
	cursor = connection.cursor()
	cursor.execute("select * from doctor where reg_no='"+str(request.session['doctorid'])+"'")
	doctor = cursor.fetchone()
	did = doctor[0]
	cursor.execute("select consultation.*,doctor.*,category.name from consultation join doctor join category  where consultation.id_category = category.category_id and consultation.doctorid = doctor.doctor_id and  consultation.status ='active' and consultation.doctorid = '"+str(did)+"'")
	adata = cursor.fetchall()
	print(adata)
	sdata=[]
	for i in adata:
		j=[]
		cursor.execute("select * from enquiry_details where consult_id='"+str(i[0])+"' and status ='requested'")
		requenquiry=cursor.fetchone()
		if requenquiry is not None:
			j.append(i[0])
			j.append(i[1])
			j.append(i[2])
			j.append(i[3])
			j.append(i[4])
			j.append(i[5])
			j.append(i[6])
			j.append(i[7])
			j.append(i[8])
			j.append(i[9])
			j.append(i[10])
			j.append(i[11])
			j.append(i[12])
			j.append(i[13])
			j.append(i[14])
			j.append(i[15])
			j.append(i[16])
			j.append("view_user_enquiry")
			j.append("view")
			j=tuple(j)
			sdata.append(j)
	sdata = tuple(sdata)


	cursor.execute("select consultation.*,doctor.*,category.name from consultation join doctor join category  where consultation.id_category = category.category_id and consultation.doctorid = doctor.doctor_id and  consultation.status ='complete' and consultation.doctorid = '"+str(did)+"'")
	bdata = cursor.fetchall()
	cdata=[]
	for i in bdata:
		j=[]

		cursor.execute("select * from enquiry_details where consult_id='"+str(i[0])+"' and status='home_remedy'")
		home_remedy =cursor.fetchone()
		if home_remedy is not None:
			j.append(i[0])
			j.append(i[1])
			j.append(i[2])
			j.append(i[3])
			j.append(i[4])
			j.append(i[5])
			j.append(i[6])
			j.append(i[7])
			j.append(i[8])
			j.append(i[9])
			j.append(i[10])
			j.append(i[11])
			j.append(i[12])
			j.append(i[13])
			j.append(i[14])
			j.append(i[15])
			j.append(i[16])
			j.append("doctor_view_home_remedies")
			j.append("Home Remedies")

		cursor.execute("select * from enquiry_details where consult_id='"+str(i[0])+"' and status='medicine_prescription'")
		medicine_pres=cursor.fetchone()
		if medicine_pres is not None:
			j.append(i[0])
			j.append(i[1])
			j.append(i[2])
			j.append(i[3])
			j.append(i[4])
			j.append(i[5])
			j.append(i[6])
			j.append(i[7])
			j.append(i[8])
			j.append(i[9])
			j.append(i[10])
			j.append(i[11])
			j.append(i[12])
			j.append(i[13])
			j.append(i[14])
			j.append(i[15])
			j.append(i[16])
			j.append("doctor_view_medicine_prescription")
			j.append("Medicine Prescription")

		
		j=tuple(j)
		cdata.append(j)
	cdata = tuple(cdata)


	cursor = connection.cursor()
	cursor.execute("select * from doctor where reg_no='"+str(request.session['doctorid'])+"'")
	doctor = cursor.fetchone()
	leave_status=doctor[8]
	if leave_status =='available':
		status='available'
		scol='greenyellow'
	elif leave_status=='not available':
		status ='Not Available'
		scol='red'
	print(sdata)
	print(cdata)
	return render(request,'doctor/consultations.html',{'adata':sdata,'status':status,'scol':scol,'bdata':cdata})


def doctor_view_home_remedies(request,id):
	cursor = connection.cursor()
	cursor.execute("select * from doctor where reg_no='"+str(request.session['doctorid'])+"'")
	doctor = cursor.fetchone()
	did = doctor[0]
	cursor.execute("select enquiry_details.*,doctor.*,category.name, m.* from enquiry_details join doctor join category join home_remedies as m where enquiry_details.consult_id='"+str(id)+"' and enquiry_details.category_id = category.category_id and enquiry_details.doctor_id = doctor.doctor_id and enquiry_details.doctor_id='"+str(did)+"'and enquiry_details.enquiry_details_id = m.enquiry_details_id ")
	adata = cursor.fetchone()
	print(adata)
	cursor.execute("select * from category where category_id='"+str(adata[6])+"'")
	cat = cursor.fetchone()

	leave_status=doctor[8]
	if leave_status =='available':
		status='available'
		scol='greenyellow'
	elif leave_status=='not available':
		status ='Not Available'
		scol='red'
	return render(request,'doctor/view_home_remedies.html',{'adata':adata,'cat':cat,'doctor':doctor,'status':status,'scol':scol})	

def doctor_view_medicine_prescription(request,id):
	cursor = connection.cursor()
	cursor.execute("select * from doctor where reg_no='"+str(request.session['doctorid'])+"'")
	doctor = cursor.fetchone()
	did = doctor[0]
	cursor.execute("select enquiry_details.*,doctor.*,category.name, m.* from enquiry_details join doctor join category join medicine_prescription as m where enquiry_details.consult_id='"+str(id)+"' and enquiry_details.category_id = category.category_id and enquiry_details.doctor_id = doctor.doctor_id and enquiry_details.doctor_id='"+str(did)+"'and enquiry_details.enquiry_details_id = m.enquiry_details_id ")
	adata = cursor.fetchone()
	print(adata)
	cursor.execute("select * from category where category_id='"+str(adata[6])+"'")
	cat = cursor.fetchone()

	leave_status=doctor[8]
	if leave_status =='available':
		status='available'
		scol='greenyellow'
	elif leave_status=='not available':
		status ='Not Available'
		scol='red'
	return render(request,'doctor/view_med_prescription.html',{'adata':adata,'cat':cat,'doctor':doctor,'status':status,'scol':scol})

def doctor_view_bill(request,id):
	cursor = connection.cursor()
	cursor.execute("select * from medicine_prescription where enquiry_details_id='"+str(id)+"' and status ='not set'")
	data = cursor.fetchone()
	if data is not None:
		cursor.execute("select * from enquiry_details where enquiry_details_id='"+str(id)+"'")
		enq= cursor.fetchone()
		consultid= str(enq[1])
		return HttpResponse("<script>alert('Not Yet Billed'); window.location='../doctor_view_medicine_prescription/%s';</script>" % consultid)
	cursor.execute("select * from medicine_prescription where enquiry_details_id='"+str(id)+"' and status ='requested'")
	data = cursor.fetchone()
	if data is not None:
		cursor.execute("select * from enquiry_details where enquiry_details_id='"+str(id)+"'")
		enq= cursor.fetchone()
		consultid= str(enq[1])
		return HttpResponse("<script>alert('Not Yet Billed'); window.location='../doctor_view_medicine_prescription/%s';</script>" % consultid)
	cursor.execute("select * from medicine_prescription as m join enquiry_details as e join doctor as d join category as c join common_staff as co where co.staff_id = m.staff_id and m.enquiry_details_id='"+str(id)+"' and m.status ='approved' and m.enquiry_details_id = e.enquiry_details_id and e.doctor_id = d.doctor_id and e.category_id = c.category_id")
	data = cursor.fetchone()
	print(data)
	if data is not None:
		cursor.execute("select * from prescription_bill where medicine_prescription_id='"+str(data[0])+"'")
		presbill = cursor.fetchone()
		total=float(presbill[2])+float(presbill[3])
		cursor.execute("select * from doctor where reg_no='"+str(request.session['doctorid'])+"'")
		doctor = cursor.fetchone()
		leave_status=doctor[8]
		if leave_status =='available':
			status='available'
			scol='greenyellow'
		elif leave_status=='not available':
			status ='Not Available'
			scol='red'
		return render(request,'doctor/payment_for_medicine_bill.html',{'data':data,'total':total,'bill':presbill,'doctor':doctor,'status':status,'scol':scol})
	cursor.execute("select * from medicine_prescription as m join enquiry_details as e join doctor as d join category as c join common_staff as co where co.staff_id = m.staff_id and m.enquiry_details_id='"+str(id)+"' and m.status ='paid' and m.enquiry_details_id = e.enquiry_details_id and e.doctor_id = d.doctor_id and e.category_id = c.category_id")	
	data = cursor.fetchone()
	print(data)
	if data is not None:
		cursor.execute("select * from prescription_bill where medicine_prescription_id='"+str(data[0])+"'")
		presbill = cursor.fetchone()
		total=float(presbill[2])+float(presbill[3])
		cursor.execute("select * from doctor where reg_no='"+str(request.session['doctorid'])+"'")
		doctor = cursor.fetchone()
		leave_status=doctor[8]
		if leave_status =='available':
			status='available'
			scol='greenyellow'
		elif leave_status=='not available':
			status ='Not Available'
			scol='red'
		return render(request,'doctor/view_medicine_bill.html',{'data':data,'total':total,'bill':presbill,'doctor':doctor,'status':status,'scol':scol})



def view_user_enquiry(request,id):
	cursor = connection.cursor()
	cursor.execute("select * from doctor where reg_no='"+str(request.session['doctorid'])+"'")
	doctor = cursor.fetchone()
	did = doctor[0]
	cursor.execute("select enquiry_details.*,doctor.*,category.name from enquiry_details join doctor join category where enquiry_details.consult_id='"+str(id)+"' and enquiry_details.category_id = category.category_id and enquiry_details.doctor_id = doctor.doctor_id and enquiry_details.doctor_id='"+str(did)+"' ")
	adata = cursor.fetchone()
	cursor.execute("select * from category where category_id='"+str(adata[6])+"'")
	cat = cursor.fetchone()

	cursor = connection.cursor()
	cursor.execute("select * from doctor where reg_no='"+str(request.session['doctorid'])+"'")
	doctor = cursor.fetchone()
	leave_status=doctor[8]
	if leave_status =='available':
		status='available'
		scol='greenyellow'
	elif leave_status=='not available':
		status ='Not Available'
		scol='red'
	return render(request,'doctor/enquiry_not_replied.html',{'adata':adata,'cat':cat,'doctor':doctor,'status':status,'scol':scol})


def add_home_remedies(request,id):
	cursor = connection.cursor()
	cursor.execute("select * from doctor where reg_no='"+str(request.session['doctorid'])+"'")
	doctor = cursor.fetchone()
	did = doctor[0]
	if request.method == "POST":
		user = request.POST['user']
		medtake = request.POST['medtake']
		disease = request.POST['disease']

		cursor.execute("insert into home_remedies values(null,'" + str(user) + "',curdate(),'"+str(disease)+"','"+str(medtake)+"','"+str(id)+"') ")
		cursor.execute("update enquiry_details set status ='home_remedy' where enquiry_details_id ='"+id+"'")
		cursor.execute("select * from enquiry_details where enquiry_details_id ='"+id+"'")
		enq = cursor.fetchone()
		cursor.execute("update consultation set status = 'complete' where id_consultation ='"+str(enq[1])+"'")
		return HttpResponse("<script> alert('Home Remedies Added');window.location='../doctor_home';</script>")	   

	cursor.execute("select enquiry_details.*,doctor.*,category.name from enquiry_details join doctor join category where enquiry_details.enquiry_details_id='"+str(id)+"' and enquiry_details.category_id = category.category_id and enquiry_details.doctor_id = doctor.doctor_id and enquiry_details.doctor_id='"+str(did)+"' ")
	adata = cursor.fetchone()
	cursor.execute("select * from category where category_id='"+str(adata[6])+"'")
	cat = cursor.fetchone()

	cursor = connection.cursor()
	cursor.execute("select * from doctor where reg_no='"+str(request.session['doctorid'])+"'")
	doctor = cursor.fetchone()
	leave_status=doctor[8]
	if leave_status =='available':
		status='available'
		scol='greenyellow'
	elif leave_status=='not available':
		status ='Not Available'
		scol='red'
	return render(request,'doctor/add_home_remedies.html',{'adata':adata,'cat':cat,'doctor':doctor,'status':status,'scol':scol})

def add_med_prescription(request,id):
	cursor = connection.cursor()
	cursor.execute("select * from doctor where reg_no='"+str(request.session['doctorid'])+"'")
	doctor = cursor.fetchone()
	did = doctor[0]
	if request.method == "POST" and request.FILES['upload']:
		user = request.POST['user']
		medtake = request.POST['medtake']
		disease = request.POST['disease']
		upload = request.FILES['upload']
		fss = FileSystemStorage()
		file = fss.save(upload.name, upload)
		file_url = fss.url(file)
		cursor.execute("insert into medicine_prescription values(null,'" + str(user) + "',curdate(),'" + str(file) + "','" + str(medtake) + "','not set','"+str(disease)+"','not set','"+str(id)+"','not set') ")
		cursor.execute("update enquiry_details set status ='medicine_prescription' where enquiry_details_id ='"+id+"'")
		cursor.execute("select * from enquiry_details where enquiry_details_id ='"+id+"'")
		enq = cursor.fetchone()
		cursor.execute("update consultation set status = 'complete' where id_consultation ='"+str(enq[1])+"'")
		return HttpResponse("<script> alert('Medicine Prescription Added');window.location='../doctor_home';</script>")	   

	cursor.execute("select enquiry_details.*,doctor.*,category.name from enquiry_details join doctor join category where enquiry_details.enquiry_details_id='"+str(id)+"' and enquiry_details.category_id = category.category_id and enquiry_details.doctor_id = doctor.doctor_id and enquiry_details.doctor_id='"+str(did)+"' ")
	adata = cursor.fetchone()
	cursor.execute("select * from category where category_id='"+str(adata[6])+"'")
	cat = cursor.fetchone()

	cursor = connection.cursor()
	cursor.execute("select * from doctor where reg_no='"+str(request.session['doctorid'])+"'")
	doctor = cursor.fetchone()
	leave_status=doctor[8]
	if leave_status =='available':
		status='available'
		scol='greenyellow'
	elif leave_status=='not available':
		status ='Not Available'
		scol='red'
	return render(request,'doctor/add_med_prescription.html',{'adata':adata,'cat':cat,'doctor':doctor,'status':status,'scol':scol})

def doctor_logout(request):
	cursor = connection.cursor()
	cursor.execute("select * from doctor where reg_no='"+str(request.session['doctorid'])+"'")
	doctor = cursor.fetchone()
	leave_status=doctor[8]
	if leave_status =='available':
		status='available'
		scol='greenyellow'
	elif leave_status=='not available':
		status ='Not Available'
		scol='red'
	return render(request,'doctor/LogOut.html',{'status':status,'scol':scol})

def staff_home(request):
	cursor = connection.cursor()
	cursor.execute("select * from common_staff where reg_no='"+str(request.session['staffid'])+"'")
	staff = cursor.fetchone()
	leave_status=staff[8]
	if leave_status =='available':
		status='available'
		scol='greenyellow'
	elif leave_status=='not available':
		status ='Not Available'
		scol='red'
	return render(request,'staff/index1.html',{'status':status,'scol':scol})

def staff_bill_history(request):
	cursor = connection.cursor()
	cursor.execute("select * from common_staff where reg_no='"+str(request.session['staffid'])+"'")
	staff = cursor.fetchone()
	cursor.execute("select * from medicine_prescription as m join enquiry_details as e join doctor as d join category as c join prescription_bill as p   where  m.status = 'paid' and m.staff_id ='"+str(staff[0])+"' and m.enquiry_details_id = e.enquiry_details_id and e.doctor_id= d.doctor_id and e.category_id= c.category_id  and m.medicine_prescription_id = p.medicine_prescription_id and p.status='Shipped' or m.status = 'paid' and m.staff_id ='"+str(staff[0])+"' and m.enquiry_details_id = e.enquiry_details_id and e.doctor_id= d.doctor_id and e.category_id= c.category_id  and m.medicine_prescription_id = p.medicine_prescription_id and p.status='Processing' ")
	data =cursor.fetchall()
	sata = []
	for i in data:
		s=list(i)
		billamount=i[32]
		shipcharge=i[33]
		s.append(billamount)
		s.append(shipcharge)
		total=float(billamount)+float(shipcharge)
		s.append(str(total))
		sata.append(s)	
	sata = tuple(sata)
	print(sata)
	leave_status=staff[8]
	if leave_status =='available':
		status='available'
		scol='greenyellow'
	elif leave_status=='not available':
		status ='Not Available'
		scol='red'
	return render(request,'staff/staff_bill_history.html',{'data':sata,'status':status,'scol':scol})

def savail_or_not(request):
	cursor = connection.cursor()
	if request.method=='POST':
		stat = request.POST['status']
		if stat=='available':
			cursor.execute("update common_staff set leave_status ='not available' where reg_no='"+str(request.session['staffid'])+"'")
		elif stat=='not available':
			cursor.execute("update common_staff set leave_status='available' where reg_no='"+str(request.session['staffid'])+"'")
	cursor.execute("select * from common_staff where reg_no='"+str(request.session['staffid'])+"'")
	staff = cursor.fetchone()
	leave_status=staff[8]
	if leave_status =='available':
		status='available'
		scol='greenyellow'
	elif leave_status=='not available':
		status ='not available'
		scol='red'
		
	return render(request,'staff/avail_or_not.html',{'status':status,'scol':scol})


def medicine_request(request):
	cursor = connection.cursor()
	cursor.execute("select * from common_staff where reg_no='"+str(request.session['staffid'])+"'")
	staff = cursor.fetchone()
	cursor.execute("select * from medicine_prescription where  status = 'requested' and staff_id ='"+str(staff[0])+"'")
	data = cursor.fetchone()
	if data ==None:
		return HttpResponse("<script> alert('No Requests Yet');window.location='../staff_home';</script>")	   
	cursor.execute("select * from medicine_prescription as m join enquiry_details as e join doctor as d join category as c where  m.status = 'requested' and m.staff_id ='"+str(staff[0])+"' and m.enquiry_details_id = e.enquiry_details_id and e.doctor_id= d.doctor_id and e.category_id= c.category_id")
	data = cursor.fetchall()
	print(data)
	leave_status=staff[8]
	if leave_status =='available':
		status='available'
		scol='greenyellow'
	elif leave_status=='not available':
		status ='Not Available'
		scol='red'
	return render(request,'staff/medicine_request.html',{'data':data,'status':status,'scol':scol})


def make_bill(request,id):
	cursor = connection.cursor()
	if request.method=='POST':
		billamount = request.POST['total']
		shipping = request.POST['shipcharge']
		cursor.execute("select * from prescription_bill where medicine_prescription_id='"+str(id)+"'")
		bill = cursor.fetchone()
		if bill is not None:
			return HttpResponse("<script> alert('Bill Already Added');window.location='../staff_home';</script>")	
		cursor.execute("insert into prescription_bill values(null,'"+str(id)+"','"+str(billamount)+"','"+str(shipping)+"','Processing')")  
		cursor.execute("update medicine_prescription set status='approved'where medicine_prescription_id='"+str(id)+"'") 
		return HttpResponse("<script> alert('Bill  Added');window.location='../medicine_request';</script>")	
	cursor.execute("select * from common_staff where reg_no='"+str(request.session['staffid'])+"'")
	staff = cursor.fetchone()
	cursor.execute("select * from medicine_prescription as m join enquiry_details as e join doctor as d join category as c where  m.status = 'requested' and m.staff_id ='"+str(staff[0])+"' and m.enquiry_details_id = e.enquiry_details_id and e.doctor_id= d.doctor_id and e.category_id= c.category_id and m.medicine_prescription_id ='"+str(id)+"'")
	data = cursor.fetchone()
	print(data)
	leave_status=staff[8]
	if leave_status =='available':
		status='available'
		scol='greenyellow'
	elif leave_status=='not available':
		status ='Not Available'
		scol='red'
	return render(request,'staff/make_bill.html',{'data':data,'status':status,'scol':scol})
	
def shipping_request(request):
	cursor = connection.cursor()
	cursor.execute("select * from common_staff where reg_no='"+str(request.session['staffid'])+"'")
	staff = cursor.fetchone()
	cursor.execute("select * from medicine_prescription as m join prescription_bill as p where  m.status = 'paid' and m.staff_id ='"+str(staff[0])+"' and p.status='Processing' and m.medicine_prescription_id = p.medicine_prescription_id ")
	data = cursor.fetchone()
	if data ==None:
		return HttpResponse("<script> alert('No Requests Yet');window.location='../staff_home';</script>")	   
	cursor.execute("select * from medicine_prescription as m join enquiry_details as e join doctor as d join category as c join prescription_bill as p   where  m.status = 'paid' and m.staff_id ='"+str(staff[0])+"' and m.enquiry_details_id = e.enquiry_details_id and e.doctor_id= d.doctor_id and e.category_id= c.category_id and p.status='Processing' and m.medicine_prescription_id = p.medicine_prescription_id ")
	data = cursor.fetchall()
	print(data)
	leave_status=staff[8]
	if leave_status =='available':
		status='available'
		scol='greenyellow'
	elif leave_status=='not available':
		status ='Not Available'
		scol='red'
	return render(request,'staff/shipping_request.html',{'data':data,'status':status,'scol':scol})

def ship_medicine(request,id):
	cursor= connection.cursor()
	cursor.execute("update prescription_bill set status='Shipped' where medicine_prescription_id='"+str(id)+"'")
	return HttpResponse("<script> alert('Shipped Medicine');window.location='../shipping_request';</script>")	   


def staff_logout(request):
	cursor = connection.cursor()
	cursor.execute("select * from common_staff where reg_no='"+str(request.session['staffid'])+"'")
	staff = cursor.fetchone()
	leave_status=staff[8]
	if leave_status =='available':
		status='available'
		scol='greenyellow'
	elif leave_status=='not available':
		status ='Not Available'
		scol='red'
	return render(request,'staff/LogOut.html',{'status':status,'scol':scol})
def user_home(request):

    return render(request,'user/index1.html')

def view_services(request):
	cursor = connection.cursor()
	cursor.execute("select * from category")
	data=cursor.fetchall()
	cursor.close()
	connection.close()
	return render(request,"user/admin_view_department.html",{'cdata':data})

def add_consultation(request,id):
	cursor = connection.cursor()
	cursor.execute("select * from category where category_id='"+id+"'")
	cat = cursor.fetchone()
	cursor.execute("select * from doctor where leave_status='available'")
	doctor = cursor.fetchall()
	if request.method == "POST":
		doctor= request.POST['doctor']
		fees = request.POST['fees']
		enquiry = (id,doctor,fees)
		return render(request,'user/pay_consultation_fee.html',{'enquiry':enquiry})
	return render(request,'user/add_consultation.html',{'cat':cat,'doctor':doctor})


def make_payment(request):
	user = request.session['uid']
	if request.method == "POST":
		card_expiry_date = request.POST['card_expiry_date']
		card_number = request.POST['card_number']
		card_holder_name = request.POST['card_holder_name']
		card_cvv = request.POST['card_cvv']
		cid = request.POST['cid']
		did = request.POST['did']
		fees = request.POST['fees']
		cursor = connection.cursor()
		cursor.execute("select * from account_table where card_number='" + card_number + "' and card_holder_name='" + card_holder_name + "' and  card_expiry_date='" + card_expiry_date + "'  and  card_cvv='" + card_cvv + "' ")
		data =cursor.fetchone()
		if data ==None:
			return HttpResponse("<script>alert('incorrect payment details');window.location='/user_home';</script>")
		else:
			cursor.execute("insert into consultation values(null,'"+cid+"','"+str(request.session['uid'])+"','"+str(did)+"',curdate(),'"+str(fees)+"','active')")
			# cursor.execute("update user_register set status='payed' where user_id='" + str(user) + "'")
			return HttpResponse("<script>alert('Paid');window.location='/user_home';</script>")
		



def consultations(request):
	cursor = connection.cursor()
	cursor.execute("select consultation.*,doctor.*,category.name from consultation join doctor join category  where consultation.id_category = category.category_id and consultation.doctorid = doctor.doctor_id and consultation.user_id='"+str(request.session['uid'])+"' and consultation.status ='active'")
	adata = cursor.fetchall()
	sdata=[]
	for i in adata:
		j=[]
		cursor.execute("select * from enquiry_details where consult_id = '"+str(i[0])+"'")
		noenquiry=cursor.fetchone()
		if noenquiry ==None:
			j.append(i[0])
			j.append(i[1])
			j.append(i[2])
			j.append(i[3])
			j.append(i[4])
			j.append(i[5])
			j.append(i[6])
			j.append(i[7])
			j.append(i[8])
			j.append(i[9])
			j.append(i[10])
			j.append(i[11])
			j.append(i[12])
			j.append(i[13])
			j.append(i[14])
			j.append(i[15])
			j.append(i[16])
			j.append("add_enquiry")
			j.append("send enquiry")
		cursor.execute("select * from enquiry_details where consult_id='"+str(i[0])+"' and status ='requested'")
		requenquiry=cursor.fetchone()
		if requenquiry is not None:
			j.append(i[0])
			j.append(i[1])
			j.append(i[2])
			j.append(i[3])
			j.append(i[4])
			j.append(i[5])
			j.append(i[6])
			j.append(i[7])
			j.append(i[8])
			j.append(i[9])
			j.append(i[10])
			j.append(i[11])
			j.append(i[12])
			j.append(i[13])
			j.append(i[14])
			j.append(i[15])
			j.append(i[16])
			j.append("enquiry_not_replied")
			j.append("view enquiry")

		j=tuple(j)
		sdata.append(j)
	sdata = tuple(sdata)
	
	print(sdata)


	cursor = connection.cursor()
	cursor.execute("select consultation.*,doctor.*,category.name from consultation join doctor join category  where consultation.id_category = category.category_id and consultation.doctorid = doctor.doctor_id and consultation.user_id='"+str(request.session['uid'])+"' and consultation.status ='complete'")
	bdata = cursor.fetchall()
	cdata=[]
	for i in bdata:
		j=[]

		cursor.execute("select * from enquiry_details where consult_id='"+str(i[0])+"' and status='home_remedy'")
		home_remedy =cursor.fetchone()
		if home_remedy is not None:
			j.append(i[0])
			j.append(i[1])
			j.append(i[2])
			j.append(i[3])
			j.append(i[4])
			j.append(i[5])
			j.append(i[6])
			j.append(i[7])
			j.append(i[8])
			j.append(i[9])
			j.append(i[10])
			j.append(i[11])
			j.append(i[12])
			j.append(i[13])
			j.append(i[14])
			j.append(i[15])
			j.append(i[16])
			j.append("view_home_remedies")
			j.append("Home Remedies")

		cursor.execute("select * from enquiry_details where consult_id='"+str(i[0])+"' and status='medicine_prescription'")
		medicine_pres=cursor.fetchone()
		if medicine_pres is not None:
			j.append(i[0])
			j.append(i[1])
			j.append(i[2])
			j.append(i[3])
			j.append(i[4])
			j.append(i[5])
			j.append(i[6])
			j.append(i[7])
			j.append(i[8])
			j.append(i[9])
			j.append(i[10])
			j.append(i[11])
			j.append(i[12])
			j.append(i[13])
			j.append(i[14])
			j.append(i[15])
			j.append(i[16])
			j.append("view_medicine_prescription")
			j.append("Medicine Prescription")

		
		j=tuple(j)
		cdata.append(j)
	cdata = tuple(cdata)
	return render(request,'user/consultations.html',{'adata':sdata,'bdata':cdata})

def add_enquiry(request,id):
	cursor = connection.cursor()
	cursor.execute("select consultation.*,doctor.*,category.name from consultation join doctor join category where consultation.id_category = category.category_id and consultation.doctorid = doctor.doctor_id and consultation.user_id='"+str(request.session['uid'])+"' and consultation.status ='active' and consultation.id_consultation='"+str(id)+"'")
	adata = cursor.fetchone()

	cursor = connection.cursor()
	cursor.execute("select * from category where category_id='"+str(adata[1])+"'")
	cat = cursor.fetchone()
	cursor.execute("select * from doctor where doctor_id='"+str(adata[3])+"'")
	doctor = cursor.fetchone()
	if request.method == "POST":
		description= request.POST['description']
		cursor.execute("insert into enquiry_details values (null,'"+str(id)+"','"+str(request.session['uid'])+"',curdate(),'"+description+"','requested','"+str(adata[1])+"','"+str(adata[3])+"')")
		return HttpResponse("<script> alert('Enquiry Added');window.location='../user_home';</script>")	   
	return render(request,'user/add_enquiry.html',{'adata':adata,'cat':cat,'doctor':doctor})



def enquiry_not_replied(request,id):
	update_status=""
	cursor=connection.cursor()
	cursor.execute("select enquiry_details.*,doctor.*,category.name from enquiry_details join doctor join category  where enquiry_details.consult_id='"+str(id)+"' and enquiry_details.category_id = category.category_id and enquiry_details.doctor_id= doctor.doctor_id and enquiry_details.user_id='"+str(request.session['uid'])+"' and enquiry_details.status ='requested'")
	adata = cursor.fetchone()
	cursor.execute("select * from category where category_id='"+str(adata[6])+"'")
	cat = cursor.fetchone()
	cursor.execute("select * from doctor where doctor_id='"+str(adata[7])+"'")
	update_status=""
	doctor = cursor.fetchone()
	if request.method == "POST":
		description= request.POST['description']
		cursor.execute("update enquiry_details set detail_description='"+description+"' where enquiry_details_id='"+str(adata[0])+"'")
		update_status="updated"
	print(adata)
	cursor.execute("select enquiry_details.*,doctor.*,category.name from enquiry_details join doctor join category  where enquiry_details.consult_id='"+str(id)+"' and enquiry_details.category_id = category.category_id and enquiry_details.doctor_id= doctor.doctor_id and enquiry_details.user_id='"+str(request.session['uid'])+"' and enquiry_details.status ='requested'")
	adata = cursor.fetchone()
	cursor.execute("select * from category where category_id='"+str(adata[6])+"'")
	cat = cursor.fetchone()
	cursor.execute("select * from doctor where doctor_id='"+str(adata[7])+"'")
	
	return render(request,'user/enquiry_not_replied.html',{'adata':adata,'cat':cat,'doctor':doctor,'us':update_status})
	


def view_medicine_prescription(request,id):
	cursor = connection.cursor()
	cursor.execute("select enquiry_details.*,doctor.*,category.name, m.* from enquiry_details join doctor join category join medicine_prescription as m where enquiry_details.consult_id='"+str(id)+"' and enquiry_details.category_id = category.category_id and enquiry_details.doctor_id = doctor.doctor_id and enquiry_details.user_id='"+str(request.session['uid'])+"'and enquiry_details.enquiry_details_id = m.enquiry_details_id  and m.status='not set'")
	adata = cursor.fetchone()
	print(adata)
	if adata is not None:
		link="Get Medicine"
		cursor.execute("select * from category where category_id='"+str(adata[6])+"'")
		cat = cursor.fetchone()
		return render(request,'user/view_med_prescription.html',{'adata':adata,'cat':cat,'link':link})
	cursor.execute("select enquiry_details.*,doctor.*,category.name, m.* from enquiry_details join doctor join category join medicine_prescription as m where enquiry_details.consult_id='"+str(id)+"' and enquiry_details.category_id = category.category_id and enquiry_details.doctor_id = doctor.doctor_id and enquiry_details.user_id='"+str(request.session['uid'])+"'and enquiry_details.enquiry_details_id = m.enquiry_details_id  and m.status='requested'")
	adata = cursor.fetchone()
	if adata is not None:
		link="View or Update shipping address"
		cursor.execute("select * from category where category_id='"+str(adata[6])+"'")
		cat = cursor.fetchone()
		return render(request,'user/view_med_prescription.html',{'adata':adata,'cat':cat,'link':link})
	cursor.execute("select enquiry_details.*,doctor.*,category.name, m.* from enquiry_details join doctor join category join medicine_prescription as m where enquiry_details.consult_id='"+str(id)+"' and enquiry_details.category_id = category.category_id and enquiry_details.doctor_id = doctor.doctor_id and enquiry_details.user_id='"+str(request.session['uid'])+"'and enquiry_details.enquiry_details_id = m.enquiry_details_id  and m.status='approved'")
	adata = cursor.fetchone()
	if adata is not None:
		link="Make Payment for Medicine"
		cursor.execute("select * from category where category_id='"+str(adata[6])+"'")
		cat = cursor.fetchone()
		return render(request,'user/view_med_prescription.html',{'adata':adata,'cat':cat,'link':link})
	cursor.execute("select enquiry_details.*,doctor.*,category.name, m.* from enquiry_details join doctor join category join medicine_prescription as m where enquiry_details.consult_id='"+str(id)+"' and enquiry_details.category_id = category.category_id and enquiry_details.doctor_id = doctor.doctor_id and enquiry_details.user_id='"+str(request.session['uid'])+"'and enquiry_details.enquiry_details_id = m.enquiry_details_id  and m.status='paid'")
	adata = cursor.fetchone()
	if adata is not None:
		link="View  Medicine Bill"
		cursor.execute("select * from category where category_id='"+str(adata[6])+"'")
		cat = cursor.fetchone()
		return render(request,'user/view_med_prescription.html',{'adata':adata,'cat':cat,'link':link})
	
	
	
	
	
def view_home_remedies(request,id):
	cursor = connection.cursor()

	cursor.execute("select enquiry_details.*,doctor.*,category.name, m.* from enquiry_details join doctor join category join home_remedies as m where enquiry_details.consult_id='"+str(id)+"' and enquiry_details.category_id = category.category_id and enquiry_details.doctor_id = doctor.doctor_id and enquiry_details.user_id='"+str(request.session['uid'])+"'and enquiry_details.enquiry_details_id = m.enquiry_details_id ")
	adata = cursor.fetchone()
	print(adata)
	cursor.execute("select * from category where category_id='"+str(adata[6])+"'")
	cat = cursor.fetchone()

	return render(request,'user/view_home_remedies.html',{'adata':adata,'cat':cat})	

def getmedicine(request,id):
	cursor = connection.cursor()
	cursor.execute("select * from medicine_prescription where enquiry_details_id='"+str(id)+"' and status ='not set'")
	data = cursor.fetchone()
	if data is not None:
		
		if request.method=='POST':
			staffid =request.POST['staff']
			shipping=request.POST['shipping']
			cursor.execute("update medicine_prescription set staff_id='"+staffid+"' where enquiry_details_id='"+id+"'")
			cursor.execute("update medicine_prescription set shipping_address='"+shipping+"' where enquiry_details_id='"+id+"'")
			cursor.execute("update medicine_prescription set status='requested' where enquiry_details_id='"+id+"'")
			return HttpResponse("<script>alert('added shipping address and send medicine request to pharmasy'); window.location='../view_medicine_prescription/%s';</script>" % id)
		
		cursor.execute("select * from common_staff where leave_status='available'")
		staff = cursor.fetchall()
		return render(request,'user/medicine_request.html',{'data':data,'staffs':staff})
	cursor.execute("select * from medicine_prescription where enquiry_details_id='"+str(id)+"' and status ='requested'")
	data = cursor.fetchone()
	if data is not None:
		if request.method=='POST':
			shipping=request.POST['shipping']
			cursor.execute("update medicine_prescription set shipping_address='"+shipping+"' where enquiry_details_id='"+id+"'")
			return HttpResponse("<script>alert('Updated shipping address and send medicine request to pharmasy'); window.location='../view_medicine_prescription/%s';</script>" % id)
		return render(request,'user/medicineu_request.html',{'data':data})
	cursor.execute("select * from medicine_prescription as m join enquiry_details as e join doctor as d join category as c where m.enquiry_details_id='"+str(id)+"' and m.status ='approved' and m.enquiry_details_id = e.enquiry_details_id and e.doctor_id = d.doctor_id and e.category_id = c.category_id")
	data = cursor.fetchone()
	print(data)
	if data is not None:
		if request.method=='POST':
			ta=request.POST['ta']
			return render(request,'user/pay_bill.html',{'total':ta,'data':data})
		cursor.execute("select * from prescription_bill where medicine_prescription_id='"+str(data[0])+"'")
		presbill = cursor.fetchone()
		total=float(presbill[2])+float(presbill[3])
		return render(request,'user/payment_for_medicine_bill.html',{'data':data,'total':total,'bill':presbill})
	cursor.execute("select * from medicine_prescription as m join enquiry_details as e join doctor as d join category as c where m.enquiry_details_id='"+str(id)+"' and m.status ='paid' and m.enquiry_details_id = e.enquiry_details_id and e.doctor_id = d.doctor_id and e.category_id = c.category_id")	
	data = cursor.fetchone()
	if data is not None:
		cursor.execute("select * from prescription_bill where medicine_prescription_id='"+str(data[0])+"'")
		presbill = cursor.fetchone()
		total=float(presbill[2])+float(presbill[3])
		return render(request,'user/view_medicine_bill.html',{'data':data,'total':total,'bill':presbill})

def make_bill_payment(request):
	user = request.session['uid']
	if request.method == "POST":
		mpid = request.POST['mpid']
		card_expiry_date = request.POST['card_expiry_date']
		card_number = request.POST['card_number']
		card_holder_name = request.POST['card_holder_name']
		card_cvv = request.POST['card_cvv']
		cursor = connection.cursor()
		cursor.execute("select * from account_table where card_number='" + card_number + "' and card_holder_name='" + card_holder_name + "' and  card_expiry_date='" + card_expiry_date + "'  and  card_cvv='" + card_cvv + "' ")
		data =cursor.fetchone()
		if data ==None:
			return HttpResponse("<script>alert('incorrect payment details');window.location='/user_home';</script>")
		else:
			cursor.execute("update medicine_prescription set status='paid' where medicine_prescription_id='" + str(mpid) + "'")
			return HttpResponse("<script>alert('Paid');window.location='/user_home';</script>")	


def user_logout(request):
    return render(request,'user/LogOut.html')