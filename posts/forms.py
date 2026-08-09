from django import forms      # Django build-in forms
from .models import *

'''   Uses the django built-in form to assign the fields to the related model, define the fields which are require the user
to feed the data to operate. 
     The automated fields don't required to mention here, those are handled by Django itself
based on the keywords and conditions given. '''

# 'model' - Define the model where it belongs to.
# 'fields' - Overwriting the django 'fields' object, the fields access by the user needs to define here 
class CreatePostForm(forms.ModelForm):
    class Meta:
        model = UserPost                          
        fields = ["title","post","post_image"]     

class EditPostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ["title","post","post_image"]

class CreateComment(forms.ModelForm):
    class Meta:
        model = UserComment
        fields = ["comment_text"]

