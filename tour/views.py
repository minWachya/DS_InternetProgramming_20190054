from django.shortcuts import render, redirect
from .models import PackageTour, Tag
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
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
   fields = ['name', 'content', 'image', 'price', 'head_image', 'head_text', 'start_day', 'end_day', 'category']
   template_name = 'tour/packagetour_update_form.html'

   def dispatch(self, request, *args, **kwargs):
      # 로그인 되어져있는지 + 로그인된 사용자와 글 작성자가 같은지
      if request.user.is_authenticated and request.user == self.get_object().author:
         return super(PackageTourUpdate, self).dispatch(request, *args, **kwargs)
      else:
         raise PermissionDenied

   def get_context_data(self, *, object_list=None, **kwargs):
      context = super(PackageTourUpdate, self).get_context_data()
      if self.object.tags.exists():
         tags_str_list = list()
         for t in self.object.tags.all():
            tags_str_list.append(t.name)
         context['tags_str_default'] = '; '.join(tags_str_list)
      return context

   def form_valid(self, form):
      response = super(PackageTourUpdate, self).form_valid(form)
      # 기존 태그 값 지우기
      self.object.tags.clear()

      # 태그 처리
      # tags_str라는 이름 가진 input 값 가져오기
      tags_str = self.request.POST.get('tags_str')
      # 태그값 있는 경우에만
      if tags_str:
         tags_str = tags_str.strip()  # 앞뒤 공백 제거
         tags_str = tags_str.replace(',', ';')  # ,와 ;로 구분 된 태그들이 ;로만 나뉘게
         tags_list = tags_str.split(';')  # ; 기준으로 테그 나누기

         for t in tags_list:
            t = t.strip()
            # 있으면 가져오고 없으면 만들기
            tag, is_tag_created = Tag.objects.get_or_create(name=t)
            # 새로 생성된 태그는 slug도 설정(allow_unicode=True : 한글 사용 허용)
            if is_tag_created:
               tag.slug = slugify(t, allow_unicode=True)
               tag.save()
            # 포스트에 태그 추가
            self.object.tags.add(tag)
      return response


def testTicket(request):
   return render(request, 'tour/test.html')