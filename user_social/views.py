
from random import randrange
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from user_social.models import User, Post
from django.conf import settings



def index(request):
    try:
        uid = User.objects.get(email=request.session['email'])
        return render(request,'index.html',{'user_data':uid})
    except:
        return render(request,'login.html')



def register(request):
    if request.method == 'POST':
        try:
            User.objects.get(email=request.POST['email'])
            msg = 'Email Already Registered.'
            return render(request,'register_user.html',{'message':msg})
        except:
            if request.POST['password'] == request.POST['rpassword']:    
                global otp, user_data
                user_data = {
                    'fullname': request.POST['fullname'],
                    'email': request.POST['email'],
                    'password': request.POST['password'],
                }
                otp = randrange(100000,999999)
                subject = 'Email Verification Social_Media_App.'
                message = f'Your OTP is {otp}.'
                msg = 'Check Your MailBox.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'otp.html',{'message':msg})
            return render(request, 'register_user.html', {'message':'Both passwords are not same.'})
    return render(request, 'register_user.html')



def otp_fun(request):
    if request.method == 'POST':
        global otp, user_data
        if request.POST['user_otp'] == str(otp):
            User.objects.create(
                fullname = user_data['fullname'],
                email = user_data['email'],
                password = user_data['password']
            )
            msg = 'Account is Created Successfully.'
            return render(request,'login.html',{'message':msg})     
        else:
            return render(request, 'otp.html',{'message':'otp comparision error'})   
    return render(request, 'otp.html')



def login(request):
    try:
        uid = User.objects.get(email=request.session['email'])
        return render(request,'index.html',{'user_data':uid})
    except:
        if request.method == 'POST':
            try:
                uid = User.objects.get(email=request.POST['email'])
                if request.POST['password'] == uid.password:
                    request.session['email'] = request.POST['email']
                    return render(request, 'index.html',{'user_data':uid})
                return render(request,'login.html',{'message':'Inncorrect password!!'})
            except:
                message = 'Email is not registered.'
                return render(request,'login.html',{'message':message})
        return render(request,'login.html')



def logout(request):
    try:
        request.session['email']
        del request.session['email']
        return render(request,'login.html')
    except:
        return render(request,'login.html')




def forgot(request):
    if request.method == 'POST':
        try:
            uid = User.objects.get(email=request.POST['email'])
            subject = 'Forgotten Password of Social_Media_App.'
            message = f'Your Password is {uid.password}.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'], ]
            send_mail( subject, message, email_from, recipient_list )
            message = 'Check Your Mailbox.'
            return render(request, 'login.html',{'message':message})
        except:
            return render(request, 'forgot.html',{'message':'This Email is not Registered.!!'})
    return render(request, 'forgot.html')



def notification(request):
    return render(request,'login.html')



def profile(request):
    if request.method == 'POST':
        try:
            uid = User.objects.get(email=request.session['email'])
            uid.fullname = request.POST['fullname']
            if request.POST['bio']:
                uid.bio = request.POST['bio']
            if request.POST['location']:
                uid.location = request.POST['location']
            if request.POST['profession']:
                uid.profession = request.POST['profession']
            if request.FILES:
                uid.pic = request.FILES['pic']
                uid.save()
            else:
                uid.save()
            return render(request, 'profile.html',{'user_data':uid})
        except:
            return render(request,'login.html')
    else:
        uid = User.objects.get(email=request.session['email'])
        return render(request, 'profile.html', {'user_data':uid})



def add_post(request):
    if request.method == 'POST':
        c = request.POST['private_status']
        print(c)
        user_data = User.objects.get(email=request.session['email'])
        if request.POST['private_status'] == 'public':
            Post.objects.create(
                user = user_data,
                caption = request.POST['caption'],
                hashtag = request.POST['hashtag'],
                pic = request.FILES['pic'],
                private_status = False
            )
        else:
            Post.objects.create(
                user = user_data,
                caption = request.POST['caption'],
                hashtag = request.POST['hashtag'],
                pic = request.FILES['pic'],
                private_status = True
            )
        return render(request, 'add_post.html', {'msg':'Post Added Successfully!'})
    return render(request, 'add_post.html')

