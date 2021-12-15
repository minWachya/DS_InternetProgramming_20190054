from .models import Comment
from django import forms

from django.forms import Form, CharField, TextInput, \
                PasswordInput, ChoiceField, BooleanField, DecimalField, DateTimeField
from markdownx.utils import markdown
from markdownx.models import MarkdownxField


# 댓글 창
class CommentForm(forms.ModelForm):
    class Meta :
        model = Comment
        # author, areated_at 은 만들 필요 X content만 있으면 됨
        fields = ['content',]


STATES = (
    ('', '선택하기'),
    ('kr', '대한민국'),
    ('jp', '일본'),
)

class TourForm(Form):
    fields = ['name', 'content', 'image', 'price', 'head_image', 'head_text',
              'start_day', 'end_day', 'category']

    name = CharField(
        widget = TextInput(
            attrs = {'placeholder': '패키지 투어 제목을 입력해주세요.'}
        )
    )
    content = MarkdownxField()

    image = DecimalField()

    address_1 = CharField(
        label  = 'Address',
        widget = TextInput(
            attrs={'placeholder': '1234 Main St'}
        )
    )
    address_2 = CharField(
        widget = TextInput(
            attrs={'placeholder': 'Apartment'}
        )
    )
    city         = CharField()
    state        = ChoiceField(choices = STATES)
    zip_code     = CharField(label = 'Zip')
    check_me_out = BooleanField(required = False)