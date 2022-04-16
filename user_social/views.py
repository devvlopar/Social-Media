from random import randrange
from urllib import request
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from user_social.models import Follow, User, Post, Comment
from django.conf import settings as setting



def index(request):
    try:
        uid = User.objects.get(email=request.session['email'])
        posts = Post.objects.all()[::-1]
        comments = Comment.objects.all()[::-1]
        return render(request,'index.html',{'user_data':uid, 'posts':posts, 'comments':comments})
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
                email_from = setting.EMAIL_HOST_USER
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
        posts = Post.objects.all()[::-1]
        comments = Comment.objects.all()[::-1]
        return render(request,'index.html',{'user_data':uid, 'posts':posts, 'comments':comments})

    except:
        if request.method == 'POST':
            try:
                uid = User.objects.get(email=request.POST['email'])
                if request.POST['password'] == uid.password:
                    request.session['email'] = request.POST['email']
                    posts = Post.objects.all()[::-1]
                    comments = Comment.objects.all()[::-1]
                    return render(request,'index.html',{'user_data':uid, 'posts':posts, 'comments':comments})
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
            email_from = setting.EMAIL_HOST_USER
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



def comment(request,pk):
    if request.method == 'POST':
        user_data = User.objects.get(email=request.session['email']) 
        post = Post.objects.get(id=pk)
        post.comment_count += 1
        post.save()
        Comment.objects.create(user = user_data, post = post, text = request.POST['comment'])
        return redirect('index')



def other_user_profile(request,pk):
    other_user = User.objects.get(id=pk)
    session_user = User.objects.get(email=request.session['email'])
    if pk == session_user.id:
        return redirect('profile')
    else:
        
        f1 = Follow.objects.filter(who=session_user, follows_whom=other_user)
        if not f1:
            disable_follow_button = False
            # print(disable_follow_button)
            return render(request, 'other_user_profile.html', {'other_user':other_user, 'session_user':session_user, 'disable':disable_follow_button})
        else:
            disable_follow_button = True
            # print(disable_follow_button, f1)
            return render(request, 'other_user_profile.html', {'other_user':other_user, 'session_user':session_user, 'disable':disable_follow_button})



def follow(request,pk):
    other_user = User.objects.get(id=pk)
    session_user = User.objects.get(email=request.session['email'])
    if pk != session_user.id:
        Follow.objects.create(
            who = session_user,
            follows_whom = other_user,
        )
        session_user.following += 1
        other_user.followers += 1
        session_user.save()
        other_user.save()
        return redirect('other_user_profile',pk)




def unfollow(request,pk):
    other_user = User.objects.get(id=pk)
    session_user = User.objects.get(email=request.session['email'])
    Follow.objects.filter(who=session_user.id, follows_whom=pk).delete()
    session_user.following -= 1
    other_user.followers -= 1
    session_user.save()
    other_user.save()
    return redirect('other_user_profile',pk)




def change_password(request):
    if request.method == 'POST':
        user_data = User.objects.get(email=request.session['email'])
        if request.POST['password'] == request.POST['rpassword']:
            user_data.password = request.POST['password']
            user_data.save()
            del request.session['email']
            return render(request, 'login.html', {'message':'Password Changed Successfully!'})
    return render(request, 'recover-password.html')



def change_email(request):
    if request.method == 'POST':
        global email_new
        email_new = request.POST['email']
        otp = randrange(100000,999999)
        subject = 'Email Verification Social_Media_App.'
        message = f'Your OTP is {otp}.'
        email_from = setting.EMAIL_HOST_USER
        recipient_list = [request.POST['email'], ]
        send_mail( subject, message, email_from, recipient_list )
        message = 'Check Your Mailbox.'
        return render(request, 'email_otp.html',{'message':message, 'otp':otp})
    return render(request, 'change_email.html')



def email_otp(request):
    if request.method == 'POST':
        user_data = User.objects.get(email=request.session['email'])
        if request.POST['user_otp'] == request.POST['otp']:
            try:
                global email_new
                User.objects.get(email=email_new)
                return render(request, 'login.html', {'message':'Account already exist with this Email.'})
            except:
                user_data.email = email_new
                user_data.save()
                del email_new
                return render(request, 'login.html', {'message':'Email is successfully changed!'})
        return render(request, 'email_otp.html',{'otp':request.POST['otp']})
    


def like(request,pk):
    liked_post = Post.objects.get(id=pk)
    session_user = User.objects.get(email=request.session['email'])
    liked_post.likes.add(session_user)
    liked_post.likes_count += 1
    liked_post.save()
    return redirect('index')



def unlike(request,pk):
    liked_post = Post.objects.get(id=pk)
    session_user = User.objects.get(email=request.session['email'])
    liked_post.likes.remove(session_user)
    liked_post.likes_count -= 1
    liked_post.save()
    return redirect('index')



def delete_account(request):
    if request.method == 'GET':
        return render(request, 'delete_account.html')
    else:
        session_user = User.objects.get(email=request.session['email'])
        if request.POST['password'] == session_user.password:
            session_user.delete()
            return render(request, 'login.html',{'message':'Account Deleted!'})
        else:
            return render(request, 'delete_account.html',{'message':'Password is Wrong!'})