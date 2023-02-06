from .models import Post,Comment
from django import forms

# QuestionForm 작성 - subject, content
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['user']

# AnswerForm - content
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user','post','content']
