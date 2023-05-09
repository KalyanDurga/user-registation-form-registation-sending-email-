from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from django.core.mail import send_mail
from app.forms import *
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def home(request):
    username=request.session.get('username')
    d={'username':username}

    return render(request,'home.html',d)



def insert_data(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}
    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            NSUO=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            NSUO.set_password(password)
            NSUO.save()

            NSPO=pfd.save(commit=False)
            NSPO.username=NSUO
            NSPO.save()
            send_mail(
                'registation',
                'kalyandurga002@gmail.com',
                'Registation for the application is successful',
                [NSUO.email],
                fail_silently=False
            )
            return HttpResponse('Regsitration is Susssessfulll')
        else:
            return HttpResponse('Not valid')

    return render(request,'insert_data.html',d)

def user_login(request):
    if request.method=='POST':
        un=request.POST['un']
        psw=request.POST['psw']
        AUO=authenticate(username=un,password=psw)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=un
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('data is not valid')

    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}

    return render(request,'display_profile.html',d)


@login_required
def change_password(request):
    if request.method=='POST':
        psw=request.POST['pw']  
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(psw)
        UO.save()
        return HttpResponse('Password is Changed Successfully')
   

    return render(request,'change_password.html')

def forget_password(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['psw']
        UO=User.objects.get(username=username)
        UO.set_password(password)
        UO.save()
        return HttpResponse('Password Updated Successfully')

        
            
    
    return render(request,'forget_password.html')