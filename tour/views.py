from django.shortcuts import render, redirect
from .models import PackageTour
from django.views.generic import ListView, DetailView
# Create your views here.


# # FBV 방법
def index(request) :
   return render(request,'tour/index.html')


# CBV 방법
# 패키지 여행 목록 페이지
class PackageTourList(ListView):
   model = PackageTour
   ordering = '-pk'

# 패키지 여행 상세 페이지
class PackageTourDetail(DetailView) :
    model = PackageTour


def testTicket(request):
   return render(request, 'tour/test.html')