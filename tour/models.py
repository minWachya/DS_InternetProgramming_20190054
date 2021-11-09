from django.db import models
import os

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


# 패키지 여행
class PackageTour(models.Model) :
    # 여행 이름
    tour_name = models.CharField(max_length=50)
    # 내용 (무한대. 길이제한 없음)
    tour_content = models.TextField()
    # 사진
    tour_image = models.ImageField(upload_to='tour/images/%Y/%m/%d')
    # 가격
    tour_price = models.CharField(max_length=10)

    # 여행사

    # 썸네일(선택)
    head_image = models.ImageField(upload_to='tour/images/%Y/%m/%d', blank=True)
    # 요약(선택)
    head_text = models.CharField(max_length=100, blank=True)
    # 여행 시작일
    tour_start_day = models.DateTimeField()
    # 여행 종료일
    tour_end_day = models.DateTimeField()

    # 카테고리
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, blank=True)

    # 태그
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}]{self.tour_name}'

    # 상세 페이지랑 연결
    def get_absolute_url(self):
        return f'/tour/list/{self.pk}'