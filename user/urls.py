from django.urls import path
from user import views
urlpatterns = [
    path("signup/",views.signup,name="signup"),
    path("signin/",views.signin,name="signin"),
    path("logout/",views.signout,name="logout"),
    path("subscribe/",views.subscribe,name="subscribe"),
    path("plan_info/<int:id>",views.plan_info,name="plan_info"),
    path("profile/",views.profile,name="profile"),
]