from django.db import models
from django.contrib.auth.models import User

''' Model is the one that able to assign or modify the data in the database. View passes the requirements which need
to get or modify in the database are handled by model.
    Divided the model into three classes without allocating it as manytomany field to reduce the confusion, comments 
and likes  uses the reverse tracking to find the post and user with the help of the foreign key given. 

    '''

class UserPost(models.Model):
    '''
        UserPost model handles the dataset related to the posts. Each object need an fieldtype to work properly like
    user is an foreign key because that helps to identify the posts, post image, created and modified time related to that user.
    '''

    # In DateTime field,
        #   "auto_now_add" used to add the time when it was created.
        #   "auto_now" will update the time wherever there is an modification or saves again.
    # "is_edited" BooleanField is used verifies that the post went through modification to display the 'edited_on' for user.

    user =models.ForeignKey(to=User,on_delete=models.CASCADE, related_name="post")
    title = models.CharField(max_length=200,editable=True,help_text="200 charectors only allowed.",blank=True,null=False,default="")
    post= models.TextField(max_length=500, editable=True, help_text="500 charectors only allowed.")
    post_image = models.ImageField(upload_to="Posts/",editable=True,blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False, editable=False)
    
    def total_likes(self):          # Counts the total count of liks for each post.
        return self.likes.count()
    
class UserComment(models.Model):
    '''     
        UserComment model handles the data operations related to comments. It track down the owner of comment and post detail
    with the foreign key allocated. "is_edited" for the same purpose from the post, for next version the comments can be editable
    for the ownership holders.'''
    user = models.ForeignKey(to=User,on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(to= UserPost,on_delete=models.CASCADE, related_name="comments")
    comment_text = models.TextField(max_length=500, editable=True, help_text="500 charectors only allowed.",blank=True,null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False, editable=False)  

class UserLike(models.Model):
    '''
        UserLikes is special case, like/unlike don't have the obects to confirm the post has been liked/unliked. Each record in the
    database is an indicate that this user likes this post and number of users liked this particular post. But Only one record between 
    one user to one post, no more than 1.'''
    user = models.ForeignKey(to=User,on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(to= UserPost,on_delete=models.CASCADE, related_name="likes")
    created_on = models.DateTimeField(auto_now_add=True)

        