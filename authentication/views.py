from django.shortcuts import render,redirect

from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_str,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def signup(request):
    if request.method == "POST":
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        if password != confirm_password:
            messages.warning(request,"Password Is Not Matching")
            return render(request,'signup.html')
        try:
            if User.objects.get(email=email):
                messages.info(request,"Email Already Taken")
                return render(request,'signup.html')
        except Exception as identifier:
            pass

        user = User.objects.create_user(username,email,password)
        user.is_active = False
        user.save()
        email_subject = "Activate Your Account"
        message = render_to_string('activate.html',{
            'user' : 'user',
            'domain' : '127.0.0.1:8000',
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
            'token' : generate_token.make_token(user),
        })

        email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
        )

        email_message.send()
        messages.success(request,"Activate Your Account by Clicking the Link in Your Email")
        return redirect('/auth/login/')
    return render(request,'signup.html')


class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            messages.info(request,"Account Activated Successfully")
            return redirect('/auth/login/')
        return render(request,'activatefail.html')




def handlelogin(request):
    if request.method=="POST":
        username = request.POST['name']
        userpassword = request.POST['pass1']
        myuser = authenticate(username=username,password=userpassword)
        if myuser is not None:
            login(request,myuser)
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/auth/login/')
    
    return render(request,'login.html')


def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/auth/login/')