from django.shortcuts import render,redirect
import re
# from django.http import HttpResponse,FileResponse,Http404,HttpResponseRedirect
# from PIL import Image
from django.contrib import auth
from .models import Account
from django.contrib import messages
from django.db import transaction
import os
from django.conf import settings
# Create your views here.

def index(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['pass']
		user = auth.authenticate(email=email,password=password)
		if user is not None:
			auth.login(request,user)
			return redirect('chat.html')
		else:
			messages.info(request,'Invalid Password')
			return render(request,'index.html')
	else:
		return render(request,'index.html')

def register(request):
	if request.method=='POST':
		name=request.POST['Name'].strip()
		email=request.POST['email'].strip()
		phno=request.POST['phone'].strip()
		pass1=request.POST['pass1'].strip()
		pass2=request.POST['pass2'].strip()
		profile=request.FILES.get('image')
		# print(profile)
		email_regex='^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
		phno_regex="^[6-9]\d{9}$"
		pass_regex="^((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%!&])).{6,20}$"
		
		if not re.search(email_regex,email):
			messages.info(request,"Invalid Email")
			return redirect('register.html')
		elif pass1!=pass2:
			messages.info(request,"Passwords do not match")
			return redirect('register.html')
		elif Account.objects.filter(email=email):
			messages.info(request,"Email already registered")
			return redirect('register.html')
		elif not re.search(phno_regex,phno):
			messages.info(request,"Invalid Contact Number")
			return redirect('register.html')
		# elif not profile:
		# 	messages.info(request,"Please enter a image")
		# 	return redirect('register.html')
		# elif not re.search(pass_regex,pass1):
		# 	messages.info(request,"Password length must be at least 6 and must contain\n1 lowercase \n1 uppercase \n1 digit \n1 special character")
		# 	return redirect('register.html')
		else:
			# try:
			# 	with transaction.atomic():
					user=Account.objects.create_user(username=name,email=email,image=profile,phno=phno,password=pass1)
					messages.info(request,"Successfully registered")
					return render(request,'index.html')
			# except:
			# 	print(Exception)
			# 	messages.info(request,"Error Occured Please try again later!")
			# 	return redirect('register.html')
		
	else:
		return render(request,'register.html')

def chat(request):
	if request.method=='GET':
		value=request.GET.get('settings')
		search=request.GET.get('search')
		
		print(value)
		try:
			if value:
				return render(request,'chat.html',{'settings':"settings"})
			elif search:
			# search=search.strip()
				# search=search.lowercase()
				search_results=Account.objects.filter(username__icontains=search,email__icontains=search)
				return render(request,'search.html',{'search_name':search,'search_result':search_results})
			else:
				friends=Account.objects.all()
				return render(request,'chat.html',{'friends':friends})
		except:
			friends=Account.objects.all()
			return render(request,'chat.html',{'friends':friends})
		
	friends=Account.objects.all()
	return render(request,'chat.html',{'friends':friends})
	# try:
	# 	friends=Account.objects.all()
	# 	return render(request,'chat.html',{'friends':friends})
	# except:
	# 	return render(request,'index.html')

def search(request):
	if request.method=='GET':
		search=request.GET['search'].strip()
		if search:
			search_results=Account.objects.filter(email__icontains=search, username__icontains=search)
			
			return render(request,'search.html',{'search_name':search,'search_result':search_results})
		else:
			return redirect('chat.html')
	return redirect('chat.html')



def user_chat(request,email):
	print(email)
	if request.method=='GET':
		value=request.GET.get('settings')
		print(value)
		if value=='settings':
			return render(request,'/chat.html',{'settings':"settings"})
	user=Account.objects.get(email=email)
	friends=Account.objects.all()
	# return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	return render(request,"chat.html",{'chat_user':user,'friends':friends})

def logout(request):
	auth.logout(request)
	return redirect('index.html')