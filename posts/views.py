from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from.forms import *

'''
     The views in this module act as the controller layer for all post-related operations. 

     Each view receives an HTTP request, validates permissions and request data, performs the required 
    database operations through the models, and returns an appropriate response by rendering a template or 
    redirecting the user with a status message.
     
     Authentication is enforced using @login_required to ensure that only authenticated users can perform these actions. '''

@login_required                   
def show_post(request):
    ''' 
        The IDs of posts already liked by the current user are collected so the template can determine whether each Like
    button should appear as "Like" or "Unlike" without querying the database for every post.

        Posts are ordered in descending creation time so that the newest posts appear first in the user's feed,
    which matches the expected behavior of most social media platforms.
    '''

    posts = UserPost.objects.all().order_by("-created_on")        # Collects all posts and order based on 'created_on', '-' represents reverse order 

    likes = UserLike.objects.all().filter(user=request.user)      # filter out the likes records created by current user, 
    liked_post_id = [like.post.id for like in likes]              # gets the post ids in a list and passes it to the templete

    return render(request,"posts/show_posts.html",context={"posts":posts,"liked_posts_ids":liked_post_id})


@login_required
def create_post(request):

    # Validate the request.method, if True, goes inside the condition
    # 'request.POST' contains the datas and 'request.FILES' contains the files given by the user
    if request.method == "POST":
        post_form = CreatePostForm(request.POST,request.FILES,)
        '''     commit=False allows additional fields that are not entered through the form 
        (such as the authenticated user) to be assigned before the object is saved to the database.'''

        # Validates the post form if valid, links the current user as the post's owner
        # Saves the post then shows the success message before redirecting it
        # When failed, shows warning message for invalid post
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()

            messages.success(request, message="New post has been added !")
            return redirect(to="posts")
        
        messages.warning(request, message="Post is invalid !")

    # GET method collects the fields from the form 
    # renders the templete for create_post along with post data to the templete.
    post_form = CreatePostForm()
    return render(request,"posts/create_post.html",context={"post":post_form})

@login_required
def editpost(request,post_id):          # Receives the post id from the templete in post_id

    post = get_object_or_404(UserPost,id=post_id)         # get post object by post_id from database or shows 404 page
    if request.method == "POST": 
        ''' Ownership verification prevents users from modifying posts 
    created by other users, enforcing authorization at the application level.'''

        # Validates the post form if valid, links the current user as the post's owner
        # Replaces the existing post data with new one then shows the success message before redirecting it
        # When failed, shows info message for invalid post
        if request.user == post.user:
            e_form = EditPostForm(data=request.POST,files=request.FILES,instance=post)
            if e_form.is_valid():
                post.is_edited = True
                e_form.save()
                
                messages.success(request,message="Post details has been modified, successfully")
                return redirect(to="posts")
            messages.info(request, message="Unsupported file, try again.")

    # GET method renders the templete for edit post along with post data and user information to the templete.
    user = request.user
    return render(request,"posts/edit_post.html",context={"post":post,"user":user})

@login_required
def delpost(request,post_id):
        
    post = get_object_or_404(UserPost,id=post_id)       # get post object by post_id from database or shows 404 page

    if request.method == "POST":
        ''' Ownership verification prevents users from deleting posts 
        created by other users, enforcing authorization at the application level.'''
        # Verifies the request.user and the post's owner is the same
        # delete the post object which got with post.id then shows the success message before redirecting it
        # When failed, shows info message for invalid user access
        if request.user == post.user:
            post.delete()
            messages.success(request,message="Post has been deleted, successfully")
            return redirect(to="posts")
        messages.info(request, message="Access denied.")

    # GET method collects the fields from the form 
    # renders the templete for deleting post along with post information to the templete.
    return render(request,"posts/delpost.html",context={"post":post})

@login_required
def postcomment(request,post_id):
      
    post = get_object_or_404(UserPost,id=post_id)       # get post object by post_id from database or shows 404 page
    if request.method == "POST":
        ''' commit=False allows additional fields that are not entered through the form 
        (such as the authenticated user) to be assigned before the object is saved to the database.'''

        # Validates the comment form if valid, links the current user and post detail into the comment object
        # Saves the comment then shows the success message before redirecting it
        # When failed, shows info message for invalid comment
        comment_form = CreateComment(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit =False)
            comment.user = request.user
            comment.post = post
            comment.save()

            messages.success(request,message="Your comment has been added.")
            return redirect(to="posts")
        messages.info(request, message="Invalid data.")

    # GET method collects the fields from the form 
    # renders the templete of show_post along with post data and comment data to the templete.
    comment = CreateComment()
    return render(request,"posts/show_posts.html",context={"post":post,"comments":comment})

@login_required
def delcomment(request,comment_id):
    ''' Ownership verification prevents users from deleting comments 
    created by other users, enforcing authorization at the application level.'''
        
    comment = get_object_or_404(UserComment,id=comment_id)       # get comment object by comment_id from database or shows 404 page

    # Verifies the request.user and the comment's owner is the same
    # delete the comment object which got with comment.id then shows the success message before redirecting it
    # When failed, shows info message for invalid user access
    if request.user == comment.user:
        comment.delete()
        messages.success(request,message="Comment has been deleted, successfully")
        return redirect(to="posts")
    messages.info(request, message="Access denied.")
    return redirect(to="posts")
    

@login_required
def likepost(request,post_id):
    
    '''  A user can only have one like record for a particular post.
      Instead of storing a boolean field, the existence of a UserLike record represents a liked state.
      Pressing the Like button toggles this state by either creating or deleting the corresponding record.  '''
    
    post = get_object_or_404(UserPost,id=post_id)       # get post object by post_id from database or shows 404 page
    if request.method == "POST":

        # is_liked is False in the beginning
        # filters the UserLike model using current user and post 
            # If it becomes true, is_like is True
        
        is_liked = False                         

        liked = UserLike.objects.all().filter(user=request.user,post=post)

        if liked:
            is_liked = True

        # When is_liked is False, creates the object with user and post
            # Shows the success message
            #  redirects to "posts"
        # When is_liked is True, delete the object stored in "liked"
            # Shows the success message
            #  redirects to "posts"
        
        if not is_liked:
            UserLike.objects.create(user = request.user, post=post)
            messages.success(request, message="You liked the post.")
            return redirect(to="posts")

        if is_liked:
            liked.delete()
            messages.success(request, message="Unliked the post.")
            return redirect(to="posts")
        
        messages.warning(request, message="Somethings went wrong, try again later.")

