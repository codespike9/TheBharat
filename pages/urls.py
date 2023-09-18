from django.urls import path

from pages import views


urlpatterns=[
    path("",views.index,name="index"),
    path("about",views.AboutUs,name="AboutUs"),
    path('search',views.search,name='search'),
]