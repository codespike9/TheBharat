from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category
    class Meta:
        verbose_name_plural="Categories"

class News(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    report_by = models.CharField(max_length=255)
    date = models.DateTimeField()
    description= models.TextField()
    conclusion = models.CharField(max_length=255)
    like_count = models.IntegerField()
    dislike_count = models.IntegerField()
    image = models.ImageField(upload_to='cover_images')
    like= models.ManyToManyField(User,related_name="liked_news",blank=True)
    dislike= models.ManyToManyField(User,related_name="disliked_news",blank=True)
    slug=models.CharField(max_length=255,null=True,blank=True)
    editorial_pick=models.BooleanField(default=True,blank=True)

    def total_likes(self):
        return self.like.count()
    def total_dislikes(self):
        return self.dislike.count()
    def get_absolute_url(self):
        return reverse('newsDetails', args=[str(self.id),self.slug,self.report_by])
    def __str__(self):
        return self.headline
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.headline)
        return super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural="News"
    def clean_my_field(self):
        data = self.cleaned_data['styles']
        # Perform validation or cleaning logic
        return data

class Comment(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    news= models.ForeignKey(News,on_delete=models.CASCADE)
    description=models.CharField(max_length=255)
    date = models.DateTimeField()
    is_available=models.BooleanField(default=True)
    like_count=models.IntegerField(default=0,editable=True)
    dislike_count=models.IntegerField(default=0,editable=True)

    def __str__(self):
        return self.news.headline+", "+self.description

class Plans(models.Model):
    plan=models.CharField(max_length=255)
    price=models.FloatField()
    extra_features=models.BooleanField(default=True)
    soft_copy=models.BooleanField(default=True)
    weekly_magazine=models.BooleanField(default=True)

    def __str__(self):
        return self.plan
    class Meta:
        verbose_name_plural="Plans"

class Order(models.Model):
    STATUS_OPTION=[
        ("Active","Inactive")
    ]

    PAYMENT_MODES = [
        ("UPI","UPI"),
        ("Net Banking","Net Banking"),
        ("Credit Card","Credit Card"),
        ("Debit Card","Debit Card"),
    ]
    user =models.ForeignKey(User,on_delete=models.DO_NOTHING)
    plan= models.ForeignKey(Plans,on_delete=models.DO_NOTHING)
    price=models.FloatField()
    status= models.CharField(max_length=20,choices=STATUS_OPTION,default='Active')
    payment_method= models.CharField(max_length=20,choices=PAYMENT_MODES)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.user.first_name+" "+self.plan.plan
    
class Payment_Details(models.Model):
    plan_choosen=models.ForeignKey(Plans,on_delete=models.DO_NOTHING)
    razor_pay_order_id=models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_signature=models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_id=models.CharField(max_length=100,null=True,blank=True)