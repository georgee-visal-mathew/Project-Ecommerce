from django.db import models

class Categories(models.Model):
    name=models.CharField(max_length=20)
    image=models.ImageField(upload_to='images',null=True,blank=True)
    desc=models.TextField(default="")
    offprice=models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=30)
    desc=models.TextField(default='')
    image=models.ImageField(upload_to='media/products',null=True,blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
