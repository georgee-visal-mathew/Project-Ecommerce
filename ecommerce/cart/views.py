from django.shortcuts import render,redirect
from shop.models import Product
from cart.models import Cart,Payment,Order
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpResponse

@login_required
def add_to_cart(request,i):
    p=Product.objects.get(id=i)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(p.stock>0):
            cart.quantity += 1
            cart.save()
            p.stock -= 1
            p.save()
    except:
        if(p.stock):
            cart=Cart.objects.create(product=p,user=u,quantity=1)
            cart.save()
            p.stock -= 1
            p.save()

    return redirect('cart:cartview')

@login_required
def cartview(request):
    u=request.user
    cart=Cart.objects.filter(user=u)
    total=0
    for i in cart:
        total=total+(i.quantity*i.product.price)
    return render(request,'cart.html',{'cart':cart,'total':total})


def cart_minus(request,i):
    p=Product.objects.get(id=i)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(cart.quantity > 1):
            cart.quantity -= 1
            cart.save()
            p.stock += 1
            p.save()
        else:
            cart.delete()
            p.stock += 1
            p.save()
    except:
        pass
    return redirect('cart:cartview')

def cart_trash(request,i):
    p=Product.objects.get(id=i)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        cart.delete()
        p.stock += cart.quantity
        p.save()
    except:
        pass
    return redirect('cart:cartview')

import razorpay
def place_order(request):
    if(request.method=="POST"):
        phone=request.POST["ph"]
        address=request.POST["a"]
        pincode=request.POST["pin"]
        landmark=request.POST["lm"]
        u=request.user
        cart=Cart.objects.filter(user=u)
        total=0
        for i in cart:
            total=total+(i.quantity*i.product.price)
        total=int(total*100)
        client=razorpay.Client(auth=("rzp_test_vagvUoVPzlml2k","2UyeeuxtqPMhUfwUzduEZWG4"))
        response_payment=client.order.create(dict(amount=total,currency='INR'))
        print(response_payment)
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status=='created':
            payment=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            payment.save()
            for i in cart:
                o=Order.objects.create(user=u,product=i.product,no_of_items=i.quantity,phone=phone,address=address,pincode=pincode,landmark=landmark,order_id=order_id)
                o.save()
        response_payment['name']=u.username
        return render(request,"payment.html",{"payment":response_payment})
    return render(request,'placeorder.html',{})

@csrf_exempt
def payment_status(request,u):
    if(not request.user.is_authenticated):
        u = User.objects.get(username=u)
        login(request,u)
    if(request.method=="POST"):
        response=request.POST
        print(response)
        param_dict={
            "razorpay_order_id":response["razorpay_order_id"],
            "razorpay_payment_id":response["razorpay_payment_id"],
            "razorpay_signature":response["razorpay_signature"]
        }
        client=razorpay.Client(auth=("rzp_test_vagvUoVPzlml2k","2UyeeuxtqPMhUfwUzduEZWG4"))
        try:
            status=client.utility.verify_payment_signature(param_dict)
            print(status)
            ord=Payment.objects.get(order_id=response["razorpay_order_id"])
            ord.razorpay_payment_id=response["razorpay_payment_id"]
            ord.paid=True
            ord.save()
            u=User.objects.get(username=u)
            c=Cart.objects.filter(user=u)
            o=Order.objects.filter(user=u,order_id=response["razorpay_order_id"])
            for i in o:
                i.payment_status="paid"
                i.save()
            c.delete()
            return render(request,"status.html",{'status':True})

        except:
            return render(request, "status.html", {'status': False})

@login_required()
def order_view(request):
    u=request.user
    o=Order.objects.filter(user=u,payment_status="paid")
    return render(request,"orders.html",{"orders":o})