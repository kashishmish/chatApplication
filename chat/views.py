# chat/views.py
from django.shortcuts import render,redirect
from .models import Messages,Personal,PersonalMessage,Groups,OnlineOffline, Registration
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.core.mail import send_mail
from django.conf import settings
import random

def index(request):
    try:
        username=request.session['username']
        image=request.session['image']
        print(image)
        return render(request,'index.html',{'image':image})
    except:
        return render(request, 'index.html')
def register(request):
    if request.method=="POST":
        name=request.POST['name']
        em=request.POST['email']
        un=request.POST['username']
        pa=request.POST['psw']
        # print(request.POST['picture'])
        if Registration.objects.filter(username=un).exists():
            messages.info(request,"username exists")
            return redirect('register')
        elif Registration.objects.filter(email=em).exists():
            messages.info(request,"email exists")
            return redirect('register')
        else:
            otp=random.randint(100000,999999)
            subject="Account Confirmation"
            msg=f"Enter this otp on the registration page.\n{otp}"
            sender=settings.EMAIL_HOST_USER
            reciever=[em]
            x=send_mail(subject,msg,sender,reciever)
            if x==1:
                return render(request,"otp.html",{'otp':otp,'name':name,'username':un,'email':em,'password':make_password(pa)})
            else:
                print("mail not sent")
            
    else:
        return render(request,'register.html')
def otp_mail(request):
    if request.method=="POST":
        otp1=request.POST['otp1']
        otp2=request.POST['otp2']
        name=request.POST['name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        picture=None
        otp2=request.POST['otp2']
        print(picture)
        if otp1==otp2:
            user_s=Registration(username=username,name=name,email=email,password=password,img=picture)
            user_s.save()
            user_status=OnlineOffline(user_id=username,status="disconnected")
            user_status.save()
            messages.info(request,"registration successful")
            return redirect('/login')
        else:
            return redirect('/register')
def login(request):
    if request.method=="POST":
        em=request.POST['username']
        pa=request.POST['password']
        print(make_password(pa))
        try:
            item =Registration.objects.get(username=em)
        except:
            messages.info(request,"Invalid Credentials")
            return redirect('login')
        if check_password(pa, item.password):
            request.session['username']=em
            username=request.session['username']
            request.session['image']=str(item.img)
            return redirect('/')
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('login')
    else:
        return render(request,'login.html')
def logout(request):
    try:
        del request.session['username']
        return redirect('/')
    except:
        return redirect('/')
def show_users(request):
    try:
        username=request.session['username']
        image=request.session['image']
        recent_talk_1st=Personal.objects.filter(me_id=username)
        recent_talk_2nd=Personal.objects.filter(user_id=username)
        l=[]
        for i in recent_talk_1st:
            l.append(i.user)
        for i in recent_talk_2nd:
            l.append(i.me)
        recently_talked=set(l)
        print(recently_talked)
        status=OnlineOffline.objects.all().order_by('user')
        return render(request, 'show_users.html',{'status':status,'recently_talked':recently_talked,'image':image})
    except:
        return redirect("/")
def groups(request):
    image=request.session['image']
    groups=Groups.objects.all()
    return render(request, 'show_groups.html',{'groups':groups,'image':image})
def room(request, room_name):
    user_name=request.session['username']
    image=request.session['image']
    try:
        group=Groups.objects.get(room=room_name)
    except:
        group_name=Groups(room=room_name,created_by_id=user_name)
        group_name.save()
    created_by=Groups.objects.get(room=room_name)
    messages=Messages.objects.filter(room_id=room_name)
    return render(request, 'room.html', {
        'room_name': room_name,
        'user_name':user_name,
        'messages':messages,
        'created_by':created_by,
        'image':image,
    })
def personal(request,you):
    image=request.session['image']
    me=request.session['username']
    try:
        person=Personal.objects.get(me_id=me,user_id=you)
    except:
        try:
            person=Personal.objects.get(me_id=you,user_id=me)
        except:
            p=Personal(me_id=me,user_id=you)
            p.save()
            person=Personal.objects.get(me_id=me,user_id=you)
    chats=PersonalMessage.objects.filter(people_id=person.id)
    status=OnlineOffline.objects.get(user=you)
    return render(request,"personal.html",{'me':me,'you':you,'chats':chats,'status':status,'image':image})
def profile(request):
    image=request.session['image']
    username=request.session['username']
    userr=Registration.objects.get(username=username)
    if request.method=="POST":
        name=request.POST['name']
        em=userr.email
        un=username
        try:
            request.FILES['picture']
            picture=request.FILES['picture']
        except:
            picture=userr.img
        
        user=Registration.objects.get(username=username)
        user.name=name
        user.email=em
        user.username=un
        user.img=picture
        user.password=userr.password
        user.save()
        del request.session['image']
        request.session['image']=str(user.img)
        image=request.session['image']
        return render(request,"profile.html",{"userr":user,'image':image})
    else:
        return render(request,"profile.html",{"userr":userr,'image':image})
def remove_profile(request):
    username=request.session['username']
    userr=Registration.objects.get(username=username)
    picture=None
    user=Registration.objects.get(username=username)
    user.img=picture
    user.name=userr.name
    user.email=userr.email
    user.username=userr.username
    user.password=userr.password
    del request.session['image']
    request.session['image']=str(user.img)
    image=request.session['image']
    user.save()
    return render(request,"profile.html",{"userr":user,'image':image})
def change_password(request):
    image=request.session['image']
    if request.method=="POST":
        em=request.POST['email']
        pa=request.POST['pas']
        image=request.session['image']
        pas=make_password(pa)
        try:
            item =Registration.objects.get(email=em)
        except:
            messages.info(request,"Wrong Email")
            return redirect('/change_password')
        item.password=pas
        item.save()
        messages.info(request,"Password Changed Successfuly")
        return redirect('/login')
    else:
        return render(request,"change_password.html",{'image':image})
def delete_user(request,username):
    user=Registration.objects.get(username=username)
    user.delete()
    del request.session['username']
    return redirect("/login")
