from django.shortcuts import render, redirect
# Create your views here.

# # FBV 방법
def index(request) :
   return render(request,'tour/index.html')