from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, HttpResponse, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import CustomerForm
from .models import Customer
# Create your views here.


def signup_user(request):
    form=CustomerForm()
    erreur=""
    context={}
    if request.method=="POST":
        form=CustomerForm(request.POST)
        if form.is_valid():
            my_instance=form.save(commit=False)
            my_instance.password=make_password(form.cleaned_data["password"])
            my_instance.save()
            current_site=get_current_site(request)
            subject="Please activate your account"

            message=render_to_string("accounts/activations_email.html",{
                "user":my_instance,
                "domain":current_site,
                "uid":urlsafe_base64_encode(force_bytes(my_instance.pk)),
                "token":default_token_generator.make_token(my_instance)
            })
            to_email=form.cleaned_data.get("email")
            email=EmailMessage(subject,message,to=[to_email])
            email.send()

            return redirect('/accounts/signin/?command=verification&email=' + my_instance.email)
            #messages.success(request,"Registration successful")


        else:

            for erre in form.errors:
                erreur+=form.errors[erre]
            context["erreur"]=erreur
    context["form"]=form
    return render(request,'accounts/signup.html',context)

def signin_user(request):
    form=CustomerForm()
    if request.method=="POST":
        email=request.POST["email"]
        password = request.POST["password"]
        user =authenticate(email=email,password=password)
        if user:
            login(request,user)
            messages.success(request, "Log in success")
            return redirect("checkout")
        else:
            messages.error(request,"Invalid credential informations ")
            return redirect("signin_user")
    return render(request,"accounts/signin.html",{'form':form})

def logout_user(request):
    user=request.user
    logout(request)
    return redirect("index")

def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Customer.objects.get(pk=uid)
    except(TypeError, ValueError,OverflowError,Customer.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        login(request, user)
        messages.success(request,"You're logged in")
        return redirect("index")
    return HttpResponse("ERRO")

def dashboard(request):

    return render(request,'accounts/dashboard.html')

def rest(request):
    form=CustomerForm()
    context={}
    if request.method=="POST":
        if Customer.objects.filter(email=request.POST.get("email")).exists():
            user=Customer.objects.get(email__exact=request.POST.get("email"))
            current_site = get_current_site(request)
            subject = "Please activate your account"

            message = render_to_string("accounts/restpassword.html", {
                "user": user,
                "domain": current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user)
            })
            to_email = user.email
            email = EmailMessage(subject, message, to=[to_email])
            email.send()

            return redirect('/accounts/signin/?command=reset&email=' + user.email)
        else:
            pass

    context["form"]=form
    return render(request,"accounts/reset.html",context)


def restpassword(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Customer.objects.get(pk=uid)
    except(TypeError, ValueError,OverflowError,Customer.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session["uid"]=uid
        print(uid)
        messages.success(request,"Please rest your password")
        return redirect("restpage")
    else:
        messages.error(request,"this link has been expired")
        return redirect("signin_user")

def restpage(request):
    form=CustomerForm()
    context={}
    if request.method=="POST":
        password=request.POST.get("password")
        password2 = request.POST.get("password2")
        if password==password2:
            print(True)
            uid=request.session.get("uid")
            print(uid)
            user=Customer.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,"Password rest successful")
            return redirect("signin_user")
        else:
            print(False)
            messages.error(request,"Password do not match")
            return redirect("restpage")

    context["form"]=form
    return render(request,"accounts/restpage.html",context)