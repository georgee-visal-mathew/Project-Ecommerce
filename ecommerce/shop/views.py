from django.shortcuts import render
from shop.models import Categories,Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

def category(request):
    items=Categories.objects.all()
    return render(request,'category.html',{'items':items})

def product(request,i):
    item=Categories.objects.get(id=i)
    product=Product.objects.filter(category=item)
    return render(request,"product.html",{"item":item,"product":product})
def productdetails(request,i):
    p=Product.objects.get(id=i)
    return render(request,"productdetails.html",{'product':p})
def register(request):
    if(request.method=="POST"):
        u=request.POST["u"]
        p=request.POST["p"]
        cp=request.POST["cp"]
        fn=request.POST["fn"]
        ln=request.POST["ln"]
        em=request.POST["em"]
        if(p==cp):
            u=User.objects.create_user(username=u,password=p,first_name=fn,last_name=ln,email=em)
            u.save()
            return category(request)
        else:
            messages.error(request,"Passwords are not same")
    return render(request,'register.html',{})

def user_login(request):
    if (request.method == "POST"):
        u = request.POST["u"]
        p = request.POST["p"]
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return category(request)
        else:
            messages.error(request,"invalid credentials")
    return render(request,'userlogin.html',{})

def user_logout(request):
    logout(request)
    return category(request)