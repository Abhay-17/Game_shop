from django.shortcuts import render, HttpResponse , redirect,get_object_or_404
from gameshopapp.models import Product,Cart,Orders,Review
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import get_connection,EmailMessage
from django.conf import settings
import random
# Create your views here.

def index(request):
    return render(request , 'index.html')

def create_product(request):
    if request.method == 'GET' :
        return render(request , 'create_product.html')
    else:
        name = request.POST['name']
        description = request.POST['description']
        developer = request.POST['developer']
        category = request.POST['category']
        price = request.POST['price']
        image = request.FILES['image']

        p = Product.objects.create(name=name,description = description , developer = developer , category = category , price= price , image = image)

        p.save()

        return redirect('/read_product')



def read_product(request):
    if request.method == 'GET':
        read = Product.objects.all()

        context = {}
        context['data'] = read

        return render (request, 'read_product.html',context)
    else:
        name = request.POST['search']

        prod = Product.objects.get(name = name)

        return redirect(f"read_product_detail/{prod.id}")

def delete_product(request,rid) :
    p = Product.objects.filter(id = rid)
    p.delete()
    return redirect('/read_product')

def update_product(request , rid) :
    if request.method == 'GET':

        p = Product.objects.filter(id = rid)

        context = {}
        context['data'] = p

        return render(request , 'update_product.html', context)
    
    else:
        name = request.POST['name']
        description = request.POST['description']
        developer = request.POST['developer']
        category = request.POST['category']
        price = request.POST['price']
        

        p = Product.objects.filter(id=rid)

        p.update(name = name, description = description, developer = developer, category = category, price = price )
        
        return redirect('/read_product')
    


def user_register(request):
    if request.method == 'GET':
        return render(request , 'register_user.html')
    else:
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password==confirm_password:
            u = User.objects.create(username = username, first_name =first_name , last_name= last_name , email = email)
            u.set_password(password)
            u.save()
            return redirect('/')
        
        else :
            context = {}
            context['error'] = 'Password and confirm password does not match'
            return render(request , 'register.html' , context)

def user_login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username , password = password)
        if user is not None :
            login(request,user)
            return redirect('/')
        else:
            context = {}
            context['error'] ='USername and password does not match'


            return render(request,'login.html',context)
        

def user_logout(request):
        logout(request)

        return redirect('/')

@login_required(login_url = "/login")
def create_cart(request,rid):
    prod = Product.objects.get(id = rid)

    cart = Cart.objects.filter(product = prod , user = request.user).exists()
    
    if cart:
      
        return redirect('/readcart')
    
    else:
        user = User.objects.get(username = request.user)

        total_price = prod.price

        c = Cart.objects.create(product = prod, user = user , quantity = 1, total_price = total_price)
        c.save()
        return redirect('/readcart')

@login_required(login_url= '/login')
def read_cart(request):
    c = Cart.objects.filter(user = request.user)
    context={}
    context['data'] = c
    return render(request,'read_cart.html', context)

def delete_cart(request , rid):

    cart = Cart.objects.filter(id = rid)
    cart.delete()
    return redirect('/readcart')

def create_order(request , rid):

    cart = Cart.objects.get(id = rid)

    order  = Orders.objects.create(product = cart.product , user = cart.user , quantity = cart.quantity , total_price = cart.total_price)

    order.save()
    cart.delete()

    return redirect('/readcart')



def read_orders(request):
    order = Orders.objects.filter(user = request.user)
    context ={}
    context['data'] = order

    return render(request , 'read_order.html' , context)

def create_review(request,rid):
    
    prod = Product.objects.get(id = rid)

    rev = Review.objects.filter(user = request.user , product = prod).exists()

    if rev:
        return HttpResponse('Review Already Added')
    else:

        if request.method == 'GET':

            return render(request,'create_review.html')
        else:
            title = request.POST['title']
            content = request.POST['content']
            rating = request.POST['rate']
            image = request.FILES['image']

            product = Product.objects.get(id = rid)

            review = Review.objects.create(title = title , content = content ,  rating = rating , image = image , product = product, user = request.user)

            review.save()

            average = Review.objects.filter(product = prod)
            
            
            return HttpResponse('Done')
        
def read_product_detail(request ,rid):
    prod = Product.objects.filter(id = rid)

    p = Product.objects.get(id = rid)

    n = Review.objects.filter(product = p).count()

    rev = Review.objects.filter(product = p)

    sum = 0
    for x in rev :
        sum = sum + x.rating 

    try:
        avg = sum/n
        int_avg = int(sum/n)

    except:
        print('No review')

    context = {}
    context['data'] = prod

    if n ==0:
        context['avg'] ='No Review'

    else:
        context['int_avg'] = int_avg
        context['avg'] = avg
        
      
    return render(request , 'read_product_detail.html', context)


def forgot_password(request) :
    if request.method == 'GET' :
        return render(request , 'forgot_password.html')
    
    else :

        email = request.POST['email']
        
        request.session['email'] = email
        user = User.objects.filter(email =email).exists()

        if user :
        


            otp = random.randint(000000 , 999999)
            request.session['otp'] =otp

            with get_connection(
                host = settings.EMAIL_HOST,
                port = settings.EMAIL_PORT,
                
                username = settings.EMAIL_HOST_USER,
                password = settings.EMAIL_HOST_PASSWORD,

                use_tls = settings.EMAIL_USE_TLS 

            ) as connection :
                
                subject = 'Email From Django Project'
                email_from = settings.EMAIL_HOST_USER
                reception_list = [email]
                message = f"Hello , your otp is {otp} "

                EmailMessage(subject, message, email_from, reception_list, connection=connection).send()

            return  redirect('/otp_verification')
        else :
            context = {}
            context['error'] = 'User does not exist'
            return render(request , 'forgot_password.html',context)
    
def otp_verification(request):
    if request.method == 'GET':
        return render(request , 'otp.html')
    
    else:
        otp = int(request.POST['otp'])
        email_otp = int(request.session['otp'])

        if otp == email_otp:
            return redirect('/new_password')
        else:
            return HttpResponse('Not Ok')

def new_password(request):
    if request.method == 'GET':
        return render(request,'new_password.html')
    else :
        email = request.session['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password :
            user = User.objects.get(email = email)
            #n = User.objects.update(password = p.set_password(password))
            user.set_password(password)
            user.save()
            return redirect('/login')
        else :
            context = {}
            context['error'] = 'Password and confirm_password doesnot match'
            return render(request,'new_password.html',context)