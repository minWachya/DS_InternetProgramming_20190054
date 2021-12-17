from django import forms
from .models import PackageTour, Comment

from django.forms import Form, CharField, TextInput, DateTimeField, ImageField
from markdownx.models import MarkdownxField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, Field


# 댓글 창
class CommentForm(forms.ModelForm):
    class Meta :
        model = Comment
        # author, areated_at 은 만들 필요 X content만 있으면 됨
        fields = ['content',]


STATES = (
    ('kr', '대한민국'),
)

# 패키지 여행 폼
#class PackageTourForm(Form):


class PackageTourCreateForm(Form):
    class Meta:
        model = PackageTour
        fields = ['name', 'content', 'image', 'price', 'head_image', 'head_text',
                'start_day', 'end_day', 'category']
        labels = {
            'name': '페키지 여행 이름',
            'content': '내용',
            'image': '기본 이미지',
            'head_image': '썸네일',
            'price': '가격',
            'head_text': '요약',
            'start_day': '여행 시작일',
            'end_day': '여행 종료일',
            }

    name = CharField()
    content = MarkdownxField()
    start_day = DateTimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field(
                'name',
                'content',
                'start_day',
            )
        )
        self.fields['name'].label = '패키지 여행 이름'
        #self.fields['content'].label = '내용'
        self.fields['start_day'].label = '여행 시작일'
        self.helper.form_method = 'post'

        #self.helper.add_input(Submit('Submit', 'Submit', css_class='btn-primary'))