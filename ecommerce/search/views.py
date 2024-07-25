from django.shortcuts import render
from django.db.models import Q
from shop.models import Product

def search_products(request):
    product=None
    query=""
    if(request.method=="POST"):
        query=request.POST["q"]
        if query:
            product=Product.objects.filter(Q(name__icontains=query))
    return render(request,"searchres.html",{'product':product,'query':query})