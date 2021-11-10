from django.shortcuts import render, redirect
from .models import PackageTour, Tag, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify


# Create your views here.


# # FBV 방법
def index(request):
    return render(request, 'tour/index.html')


# CBV 방법
# 패키지 여행 목록 페이지
class PackageTourList(ListView):
    model = PackageTour
    ordering = '-pk'

    # 카테고리 데이터 가져오기
    def get_context_data(self, *, object_list=None, **kwargs):
        # 상위 context를 사용하겠다.
        context = super(PackageTourList, self).get_context_data()
        # 카테고리 값 모두 가져오기
        context['categories'] = Category.objects.all()
        # 카테고리 없는 포스트 갯수
        context['no_category_post_count'] = PackageTour.objects.filter(category=None).count()
        return context


# 패키지 여행 상세 페이지
class PackageTourDetail(DetailView):
    model = PackageTour

    # 카테고리 데이터 가져오기
    def get_context_data(self, *, object_list=None, **kwargs):
        # 상위 context를 사용하겠다.
        context = super(PackageTourDetail, self).get_context_data()
        # 카테고리 값 모두 가져오기
        context['categories'] = Category.objects.all()
        # 카테고리 없는 포스트 갯수
        context['no_category_post_count'] = PackageTour.objects.filter(category=None).count()
        return context


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


# 패키지 여행 생성 패아지
# 로그인 한 사람만 접근 가능 : LoginRequiredMixin
class PackageTourCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = PackageTour
    # created_at 은 자동이라 입력 X
    fields = ['name', 'content', 'image', 'price', 'head_image', 'head_text', 'start_day', 'end_day', 'category']

    # 로그인 한 사용자가 슈퍼유저나 스태프면 true 반환
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    # 로그인 한 author로 자동 설정
    def form_valid(self, form):
        current_user = self.request.user
        # 로그인 된 사용자 + 슈퍼유저/스태프 유저인지
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super(PackageTourCreate, self).form_valid(form)

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
        # 로그인 안 된 사용자
        else:
            return redirect('/tour/')


# FBV 방법
# html 어떻게 보이는지 테스트
def testTicket(request):
    return render(request, 'tour/test.html')
