from django.contrib import admin

# Register your models here.
from news.models import Category
from news.models import News,Comment,Plans,Order
from django_summernote.admin import SummernoteModelAdmin

class NewsAdmin(SummernoteModelAdmin):
    list_display=('headline','category','report_by','editorial_pick','conclusion')
    search_fields=('report_by','description','headline','conclusion')
    list_filter = ('category',)
    list_editable=('editorial_pick',)
    summernote_fields=('description',)

class PlansAdmin(admin.ModelAdmin):
    # list_display_links=('extra_features','soft_copy','weekly_magazine')
    list_display=('plan','price','extra_features','soft_copy','weekly_magazine')
    list_editable=('extra_features','soft_copy','weekly_magazine')

class OrderAdmin(admin.ModelAdmin):
    list_display=('user','plan','status')
    search_fields=('user','plan')
    list_editable=('status',)
    list_filter = ('status',)

admin.site.register(Category)
admin.site.register(News,NewsAdmin)
admin.site.register(Comment)
admin.site.register(Plans,PlansAdmin)
admin.site.register(Order,OrderAdmin)
