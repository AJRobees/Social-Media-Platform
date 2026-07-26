from django.urls import path,include
from . import views
from .models import UserPost


urlpatterns =[
    path("",views.show_post,name="posts"),
    path("new_post/",views.create_post,name="new_post"),
    path("search/",views.editpost,name="search"),
    path("edit/<int:post_id>/",views.editpost,name="edit"),
    path("<int:post_id>/delete/",views.delpost,name="delete"),
    
    ]
    