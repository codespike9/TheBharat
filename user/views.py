from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User #User Model
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators  import login_required
from news.models import News,Plans,Order,Payment_Details
from user.models import Profile
import razorpay
from django.conf import settings
# Create your views here.

@never_cache
def signup(request):
    if request.user.is_authenticated:
        return redirect('all_news')
    if request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('user_name')
        password = request.POST.get('password')

        user_exists=False

        if User.objects.filter(username=username).exists():
            messages.error(request,"Username is already taken. Try with a new username.")
            user_exists = True

        if User.objects.filter(email=email).exists():
            messages.error(request,"Email is already taken. Try with a new email.")
            user_exists = True
        if user_exists:
            return render(request,'user/signup.html')
        
        user=User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password
        )
        user.save()
        messages.success(request,"Account Created Successfully. Login to Continue")


    return render(request,'user/signup.html')
@never_cache
def signin(request):
    if request.user.is_authenticated:
        return redirect('all_news')
    if request.method=="POST":
        username = request.POST.get('user_name')
        password = request.POST.get('password')

        user_exists=False

        user = authenticate(request,username=username, password=password)
        if user is None:
            messages.error(request, "Invalid Username or Password")
            return render(request,"user/signin.html")
        else:
            login(request,user)
            return redirect("all_news")

    return render(request,'user/signin.html')

def signout(request):
    logout(request)
    return render(request,'user/signin.html')

def subscribe(request):
    plans=Plans.objects.all()
    subs=Profile.objects.filter(user=request.user)
    for subs in subs:
        print(subs.subscribe)
    context={
        'plans':plans,
        'subs':subs
    }
    return render(request, 'user/subscribe.html',context)

def plan_info(request,id):
    plan=Plans.objects.filter(id=id)
    for plans in plan:
        print(plans)
    client= razorpay.Client(auth = (settings.KEY , settings.SECRET) )
    payment= client.order.create({'amount':plans.price * 100,'currency':'INR','payment_capture':1})
    payment_details=Payment_Details(
        plan_choosen=Plans.objects.get(id=id),
        razor_pay_order_id=payment['id']
    )
    payment_details.save()
    context={
        'plan':plan,
        'payment':payment
    }
    return render(request,'news/plan_information.html',context)

@login_required(login_url="/user/signin")
def profile(request):
    subs=Profile.objects.filter(user=request.user)
    for subs in subs:
        print(subs.subscribe)
    context={
        'subs':subs
    }
    return render(request,'user/profile.html',context)


    
