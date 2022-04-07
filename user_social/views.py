import email
import re
from django.shortcuts import render

from user_social.models import User

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        try:
            User.objects.get(email=request.POST['email'])
            msg = 'Email Already Registered.'
            return render(request,'register_user.html',{'message':msg})
        except:
            


    return render(request, 'register_user.html')

def otp(request):
    if request.method == 'POST':
        if request.POST['otp'] == request.POST['user_otp']:
            pass

            
    return render(request, 'otp.html')