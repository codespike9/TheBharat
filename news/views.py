from django.shortcuts import render, get_object_or_404,redirect
from news.models import Category,News,Order,Comment,Plans
from user.models import Profile
from django.views.decorators.csrf import csrf_exempt
# from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import send_mail
import razorpay
# Create your views here.

def all_news(request):
    category=Category.objects.filter(category="Photo")
    for c in category:
        news = News.objects.exclude(category=c.id).order_by("?")[:2]
        r_news = News.objects.exclude(category=c.id).order_by("?")[:6]
    breaking_news =News.objects.exclude(category=c.id).order_by("?")[:4]
    c_news=News.objects.all().order_by("?")[:1]
    categories = Category.objects.all().order_by('category')
    specific_news=News.objects.filter(report_by = 'Entertainment Desk')
    headlines_news = News.objects.all().order_by('?')[:6]
    b_news=News.objects.all().order_by("?")[:3]
    # r_news=News.objects.all().order_by("?")[:6]
    # user=User.objects.get(id=request.user.id)
    # user.save()
    context ={
        "news":news,
        "categories":categories,
        "breaking_news":breaking_news,
        "c_news":c_news,
        "specific_news":specific_news,
        "headlines_news":headlines_news,
        "b_news":b_news,
        "r_news":r_news
    }

    return render(request,"news/news.html",context)

def category_news(request,cid):
    news=News.objects.filter(category=cid).prefetch_related('category')
    category_name=Category.objects.filter(id=cid)
    random_news=News.objects.all().order_by('?')[:3]
    categories=Category.objects.all().order_by('-category')
    context ={
        'news':news,
        'category_name':category_name,
        'random_news':random_news,
        'categories':categories,
    }

    return render(request,"news/news_category.html",context)

def comment(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            username=request.POST.get('username')
            comment=request.POST.get('comment')
            id=request.POST.get('news')
            date=request.POST.get('date')
            comment_post=   Comment(
                user=request.user,
                news=News.objects.get(id=id),
                description=comment,
                date=date
            )
            comment_post.save()
            refer=request.META.get('HTTP_REFERER')
            return redirect(refer if refer else '/default-page/')
    else:
        return render(request,"user/signin.html")

def news_details(request,id,slug_url,report):
    news=get_object_or_404(News,id=id,slug=slug_url)
    categories=Category.objects.all().order_by('-category')
    random_news=News.objects.all().order_by('?')[:4]
    news_report_by = News.objects.filter(report_by=report)
    comment=Comment.objects.filter(news=news)
    time=timezone.localtime()
    total_likes=news.total_likes()
    total_dislikes=news.total_dislikes()
    share_link = request.build_absolute_uri(news.get_absolute_url())
    like_list=news.like.all()
    dislike_list=news.dislike.all()
    context={
        "news":news,
        'random_news':random_news,
        'news_report_by':news_report_by,
        'categories':categories,
        'comment':comment,
        'time':time,
        'total_likes':total_likes,
        'total_dislikes':total_dislikes,
        'share_link':share_link,
        'like_list':like_list,
        'dislike_list':dislike_list
    }
    print(random_news)
    return render(request,"news/news_details.html",context)

def delete_comment(request,cid):
    comment=Comment.objects.filter(id=cid).delete()
    refer=request.META.get('HTTP_REFERER')
    return redirect(refer if refer else '/default-page/')
# def random_news(request):
    
#     # categories=Category.objects.all().order_by('-category')
#     context ={
        
        
#     }

#     return render(request,"news/news_details.html",context)

def like(request,id):
    if request.user.is_authenticated:
        news= get_object_or_404(News,id=id)
        news.like.add(request.user)
        dislike_count=news.total_dislikes()
        list=news.dislike.all()
        if dislike_count > 0:
            if request.user in list:
                news.dislike.remove(request.user)
        refer=request.META.get('HTTP_REFERER')
        return redirect(refer if refer else '/default-page/')
    else:
        return render(request,"user/signin.html")

def dislike(request,id):
    if request.user.is_authenticated:
        news= get_object_or_404(News,id=id)
        news.dislike.add(request.user)
        like_count=news.total_likes()
        list=news.like.all()
        if like_count > 0:
            if request.user in list:
                news.like.remove(request.user)
        refer=request.META.get('HTTP_REFERER')
        return redirect(refer if refer else '/default-page/')
    else:
        return render(request,"user/signin.html")

def buy_plan(request):
    if request.method=="POST":
        user=request.user
        plan=request.POST.get("plan")
        price=request.POST.get("price")
        payment_method=request.POST.get("payment_mode")

    print("aaaa")
    user_list=[]
    profiles=Profile.objects.all()
    for profile in profiles:
        user_list.append(profile.user)
    if user in user_list:
        profile=Profile.objects.get(user=user.id)
        profile.subscribe=Plans.objects.get(id=plan)
        profile.save()
    else:
        profile=Profile.objects.create(user=user,subscribe=Plans.objects.get(id=plan))
    orders=Order.objects.all()
    users=[]

    for order in orders:
        users.append(order.user)
    if user in users:
       order=Order.objects.get(user=user)
       order.plan=Plans.objects.get(id=plan)
       order.price=price
       payment_method=payment_method
       order.save()
    else:
        order = Order(
                plan= Plans.objects.get(id=plan),
                user=user,
                price =price,
                payment_method=payment_method,
            )
        order.save()
    plan=Plans.objects.get(id=plan).plan
    mail_context={
        "username": request.user.first_name+" "+request.user.last_name,
        "price": price,
        "plan":plan,
        "payment_method":payment_method
    }
    subject = "Plan is bought successfully"
    html_message = render_to_string('news/mail_template.html',mail_context)
    plain_message = strip_tags(html_message)
    to = [request.user.email, ]
    from_email = settings.EMAIL_HOST_USER
    # send_mail(subject=subject, message=body, from_email=from_email, recipient_list=to,fail_silently=False)
    send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=to,fail_silently=False, html_message=html_message)


    return redirect('all_news')