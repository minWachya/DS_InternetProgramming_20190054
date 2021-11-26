from django.shortcuts import render
from tour.models import Comment
from django.db.models import Q


def about_me(request):
    return render(request, 'about/me.html')


# 회사 소개
def about_us(request):
    return render(request, 'about/us.html')
