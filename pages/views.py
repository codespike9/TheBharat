from django.shortcuts import render,HttpResponse
from news.models import News,Category
import datetime ,random
# Create your views here.
def index(request):
    # return HttpResponse("<h1>Hello world</h1>")
    news=News.objects.all().order_by('?')[:1]
    category_name=Category.objects.filter(category='Entertainment')
    for c in category_name:
        en_news=News.objects.filter(category=c.id).order_by('?')[:4]
    category_name=Category.objects.filter(category='Sports')
    for c in category_name:
        sp_news=News.objects.filter(category=c.id)
    category_name=Category.objects.filter(category='War')
    for c in category_name:
        wr_news=News.objects.filter(category=c.id)
    news_all=News.objects.all()
    likes={}
    for n in news_all:
        likes[n.id]=n.total_likes()
    likes_keys=list(likes.keys())
    likes_keys.sort()
    sorted_likes={i:likes[i] for i in likes}
    id=max(zip(sorted_likes.values(),sorted_likes.keys()))[1]
    mst_liked=News.objects.filter(id=id)
    category_name=Category.objects.filter(category='Photo')
    for c in category_name:
        photo=News.objects.filter(category=c.id)[:1]
    editorial_pick=[]
    for a in news_all:
        if a.editorial_pick==True:
            editorial_pick.append(a)
    random_index=random.randint(0,len(editorial_pick)-1)
    one_editorial_pick=editorial_pick[random_index]
    category_name=Category.objects.filter(category='Business')
    for c in category_name:
        bn_news=News.objects.filter(category=c.id)
    context={
        'en_news':en_news,
        'news':news,
        'category_name':category_name,
        'sp_news':sp_news,
        'wr_news':wr_news,
        'mst_liked':mst_liked,
        'news_all':news_all[:6],
        'photo':photo,
        'sorted_likes':sorted_likes.keys(),
        'editorial_pick':editorial_pick,
        'one_editorial_pick':one_editorial_pick,
        'bn_news':bn_news
    }
    return render(request, 'pages/index.html',context)
def AboutUs(request):
    return render(request, 'pages/AboutUs.html')
def search(request):
    query=request.POST.get('query')
    if len(query) > 80 :
        news=[]
    else:
        news_headline=News.objects.filter(headline__icontains=query)
        news_desc=News.objects.filter(description__icontains=query)
        news=news_headline.union(news_desc)
    context={
        "news":news,
        # "news_des":news_des,
        "query":query
    }
    return render(request,'pages/search.html',context)
    return render(request,'pages/search.html')
