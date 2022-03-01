
from base64 import urlsafe_b64decode
from django.contrib.sites.shortcuts import get_current_site
from tokenize import generate_tokens
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import django.core.mail 
from django.template.loader import render_to_string


from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
import django.utils.encoding

# Create your views here.
@login_required
def home(request):
    return render(request, 'home.html')
def loginn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['pass1']
        us=authenticate(username=username, password=password1)
        if us is not None:
            login(request,us)
            u=User.objects.get(username=username)
            print(dir(u))
            return render(request,'home.html',{'user':us,'fname':(u)})
        else :
            messages.error(request,'ataced mn al username aw elpass')
    return render(request, 'login.html')
def logoutt(request):
    logout(request)
    messages.success(request,'you are logged out')
    return redirect('test')
    
def test(request):
    return render(request, 'test.html')

def reg(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email1 = request.POST['email']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']
        if User.objects.filter(username=username):
            messages.error(request,'The user is already exist')
            return redirect('test')
        elif User.objects.filter(email=email1):
            messages.error(request,'The Email is already Regesterid')
            return redirect('test')
        elif len(username)>10:
            messages.error(request,'the user is len than 10 characters')
            return redirect('test')
        elif password1!=password2:
            messages.error(request,'Passwords dont match')
            return redirect('test')
        elif not username.isalnum():
            messages.error(request,'must be alphabetic')
            return redirect('test')
        else:
            myuser=User.objects.create_user(username,email1,password1)
            myuser.frist_name = fname
            myuser.last_name =lname
            myuser.is_active =False

            myuser.save()
            messages.success(request,"your acc is created" )
            smail=  django.core.mail.EmailMessage(
                'hi',
                'THIS IS Auto Mail FROM Eslam Qadri',
                'ekadryahmed@gmail.com',
                [email1]
                 
            )
              
            smail.send(fail_silently= False)

            current_site = get_current_site(request)
        email_subject = "Confirm your Email @ GFG - Django Login!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': django.utils.encoding.urlsafe_base64_encode(django.utils.encoding.force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = django.core.mail.EmailMessagee(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        return redirect('test')


    return render(request, 'reg.html')
def activate(request,uidb64,token):
    try:
        uid =django.utils.encoding.force_text(urlsafe_b64decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_tokens.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')
