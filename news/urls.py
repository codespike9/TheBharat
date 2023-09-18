from django.urls import path
from news.views import all_news, category_news,news_details,like,dislike,comment,delete_comment,buy_plan


urlpatterns = [
    path("",all_news,name="all_news"),
    path("<int:id>/<str:slug_url>/<str:report>/",news_details,name="newsDetails"),
    path("category/<int:cid>/",category_news,name="news_category"),
    path('like/<int:id>/',like,name="like"),
    path('dislike/<int:id>/',dislike,name="dislike"),
    path("comment/",comment,name="comment"),
    path("<int:cid>",delete_comment,name="delete_comment"),
    path("buy_plan/",buy_plan,name="buy_plan"),
]