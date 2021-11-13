from django.db import models
import os
from markdownx.utils import markdown
from markdownx.models import MarkdownxField
from django.contrib.auth.models import User

# Create your models here.

# 태그
class Tag(models.Model):
    # 카테고리 명(중복불가:unique=True)
    # pk(숫자) 대신 name 자체(text)로 url 만들고 싶다. (한굴 포함 : allow_unicode=True)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return f'/tour/tag/{self.slug}'


# 카테고리
class Category(models.Model):
    # 카테고리 명(중복불가:unique=True)
    # pk(숫자) 대신 name 자체(text)로 url 만들고 싶다. (한굴 포함 : allow_unicode=True)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return f'/tour/category/{self.slug}'

    # admin에 뜨느 클래스 이름
    class Meta:
        verbose_name_plural = 'Categories'


# 여행사
class TourAgency(models.Model) :
    # 여행사명
    name = models.CharField(max_length=50)
    # 주소
    address = models.CharField(max_length=300)
    # 연락처
    contact_number =  models.CharField(max_length=20)
    # 여행사 로고
    logo = models.ImageField(upload_to='agency/images/%Y/%m/%d')

    def __str__(self):
        return f'[{self.pk}]{self.name}'


# 패키지 여행
class PackageTour(models.Model) :
    # 여행 이름
    name = models.CharField(max_length=50)
    # 내용 (무한대. 길이제한 없음)
    content = MarkdownxField()
    # 사진
    image = models.ImageField(upload_to='tour/images/%Y/%m/%d')
    # 가격
    price = models.CharField(max_length=10)
    # 여행사
    agency = models.ForeignKey(TourAgency, on_delete=models.CASCADE, null=True, blank=True)
    # 썸네일(선택)
    head_image = models.ImageField(upload_to='tour/images/%Y/%m/%d', blank=True)
    # 요약(선택)
    head_text = models.CharField(max_length=100, blank=True)
    # 여행 시작일
    start_day = models.DateTimeField()
    # 여행 종료일
    end_day = models.DateTimeField()
    # 카테고리
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, blank=True)
    # 태그
    tags = models.ManyToManyField(Tag, blank=True)
    # 작성자
    # CASCADE : User 삭제 시 작성한 모든 포스트도 delete + null=True
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'[{self.pk}]{self.name}'

    # 상세 페이지랑 연결
    def get_absolute_url(self):
        return f'/tour/list/{self.pk}/'

    # content 내용을 마크다운으로 변경해주는 함수
    def get_content_markdown(self):
        return markdown(self.content)


# 댓글
class Comment(models.Model):
    # 패키지 여행 id
    # 여행 게싀글글 삭제 시 포트의 댓글도 삭제 : CASCADE
    tour = models.ForeignKey(PackageTour, on_delete=models.CASCADE, null=True)
    # 댓글 작성자
    # 시용지 삭제 시 포스트의 댓글도 삭제 : CASCADE
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # 댓글 내용
    content = models.TextField()
    # 작성 시간
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    # 패키지 여행 url 리턴
    def get_absolute_url(self):
        return f'{self.tour.get_absolute_url()}#comment-{self.pk}'