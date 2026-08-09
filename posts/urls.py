from django.urls import path
from . import views

'''      Navigate the urls from the browser to get the information by directing the 
path where it want to be, constructs the urls according to the request received.'''

urlpatterns =[
    path("",views.show_post,name="posts"),                   # constructs the path that leads to the posts page for listing all posts
    path("new_post/",views.create_post,name="new_post"),        # constructs the path that leads to the create a new_post page 
    path("edit/<int:post_id>/",views.editpost,name="edit"),       # constructs the path that leads to the edit_post page
    path("<int:post_id>/delete/",views.delpost,name="delete"),      # constructs the path that leads to the delete post page for confirmation

    # '<int:post_id>' receives from the templete as integer
    path("<int:post_id>/comment/",views.postcomment,name="comments"),            # Navigate the urls to post new comment
    path("<int:comment_id>/delete/comment/",views.delcomment,name="delcomment"),   # Navigate the urls to delete the comment with it's ID

    # Navigate the urls to like or unlike the post
    path("<int:post_id>/like/",views.likepost,name="likes"),
    path("<int:like_id>/unlike/",views.likepost,name="unlike"),
    
    ]
    