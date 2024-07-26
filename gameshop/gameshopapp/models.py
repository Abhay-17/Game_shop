from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    type = (('sport' , 'sport'),('action' , 'action') , ('fighting','fighting') , ('battle royale' , 'battle royale'),('action' , 'action'),('role playing' , 'role playing'))
    name = models.CharField(max_length= 200)
    description = models.CharField(max_length= 200)
    developer = models.CharField(max_length= 200)
    category = models.CharField(max_length=200 , choices=type)    
    price = models.FloatField()
    image = models.ImageField(upload_to ='image')
    rating = models.FloatField(range(1,5))

class Cart(models.Model):
    type = ( (1,1),(2,2),(3,3),(4,4),(5,5) )
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField(choices= type)
    total_price = models.IntegerField()


class Orders(models.Model):
    
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField()

class Review(models.Model):

    type = ( (1,1),(2,2),(3,3),(4,4),(5,5) )
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    rating = models.IntegerField(choices=type)
    image = models.ImageField(upload_to= 'reviewimage')