from .models import Comment
from django import forms

# 댓글 창
class CommentForm(forms.ModelForm):
    class Meta :
        model = Comment
        # author, areated_at 은 만들 필요 X content만 있으면 됨
        fields = ['content',]