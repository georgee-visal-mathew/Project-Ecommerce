from cart.models import Cart

def cart_item(request):
    u=request.user
    c=0
    if(request.user.is_authenticated):
        try:
            cart=Cart.objects.filter(user=u)
            c=cart.count()
        except:
            c=0
    return {'count':c}

def count_item(request):
    u=request.user
    num=0
    if(request.user.is_authenticated):
        try:
            cart=Cart.objects.filter(user=u)
            for i in cart:
                num=num+i.quantity
        except:
            num=0
    return {'num':num}