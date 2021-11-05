from django.shortcuts import render, redirect
from .models import PackageTour
from django.views.generic import ListView, DetailView
# Create your views here.


# # FBV 방법
def index(request) :
   return render(request,'tour/index.html')


class PackageTourList(ListView):
   model = PackageTour
   ordering = '-pk'