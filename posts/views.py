from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from.forms import *

# Create your views here.
@login_required
def show_post(request):
    posts = UserPost.objects.all().order_by("-created_on")
    return render(request,"posts/show_posts.html",context={"posts":posts})

@login_required
def create_post(request):
    if request.method == "POST":
        post_form = CreatePostForm(request.POST,request.FILES,)

        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()

            print(request.FILES)
            print(post_form.errors)
            messages.success(request, message="New post has been added !")
            return redirect(to="posts")
        
        print(request.FILES)
        print(post_form.errors)
        messages.warning(request, message="Post is invalid !")

    post_form = CreatePostForm()
    return render(request,"posts/create_post.html",context={"post":post_form})

@login_required
def editpost(request,post_id):
    if request.method == "POST":
        post = UserPost.objects.get(id=post_id)
        if request.user == post.user:
            e_form = EditPostForm(data=request.POST,files=request.FILES,instance=post)
            if e_form.is_valid():
                post.is_edited = True
                e_form.save()
                
                messages.success(request,message="Post details has been modified, successfully")
                return redirect(to="posts")
            messages.info(request, message="Somethings went wrong, try again later.")

    user = request.user
    post = get_object_or_404(UserPost,id=post_id)
    return render(request,"posts/edit_post.html",context={"post":post,"user":user})

@login_required
def delpost(request,post_id):
    post = get_object_or_404(UserPost,id=post_id)

    if request.method == "POST":
        if request.user == post.user:
            post.delete()
            messages.success(request,message="Post has been deleted, successfully")
            return redirect(to="posts")
        messages.info(request, message="Somethings went wrong, try again later.")

    return render(request,"posts/delpost.html",context={"post":post})
