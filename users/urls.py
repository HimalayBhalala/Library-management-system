from django.urls import path
from . import views

urlpatterns = [
    path("all/",views.get_all_user,name="all-user"),
    path("profile/",views.profile,name="profile")
]
