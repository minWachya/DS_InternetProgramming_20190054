from django.shortcuts import render, redirect
from .models import PackageTour
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
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


# 레시피 수정
class PackageTourUpdate(LoginRequiredMixin, UpdateView):
   model = PackageTour
   fields = ['title', 'content']

   def dispatch(self, request, *args, **kwargs):
      # 로그인 되어져있는지 + 로그인된 사용자와 글 작성자가 같은지
      if request.user.is_authenticated and request.user == self.get_object().author:
         return super(PackageTourUpdate, self).dispatch(request, *args, **kwargs)
      else:
         raise PermissionDenied


def testTicket(request):
   return render(request, 'tour/test.html')