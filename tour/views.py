from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import PackageTour, Tag, Category, TourAgency, Comment
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.db.models import Q

# Create your views here.


# # FBV 방법
# 홈
def index(request):
    recent_tour = PackageTour.objects.order_by('-pk')[:3]
    tour0 = Comment.objects.filter(tour=recent_tour[0]).count()
    tour1 = Comment.objects.filter(tour=recent_tour[1]).count()
    tour2 = Comment.objects.filter(tour=recent_tour[2]).count()
    return render(request, 'tour/index.html',
                  {
                      'recent_tour':recent_tour,
                      'categories': Category.objects.all(),
                      'tour_agencies':TourAgency.objects.all(),
                      'tour0_comment_count':tour0,
                      'tour1_comment_count': tour1,
                      'tour2_comment_count': tour2,
                  }
                  )


# 카테고리 페이지
class CategoryList(ListView):
    model = Category
    ordering = '-pk'
    paginate_by = 6
    template_name = 'tour/packagetour_list.html.html'
class CategoryPage(CategoryList):
    # 페이지네이션 갯수
    paginate_by = 6
    ordering = '-pk'

    # 검색 결과 반환
    def get_queryset(self):
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        # 카테고리 있는 모든 포스트 불러오기(다대일 관계)
        tour_list = PackageTour.objects.filter(category=category)
        return tour_list

    # 추가적으로 전당할 데이터
    def get_context_data(self, **kwargs):
        context = super(CategoryPage, self).get_context_data()
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        context['search_info'] = '카테고리 검색'
        context['search_info_keyword'] = category.name
        context['search_info_count'] = f'총 {self.get_queryset().count()}건의 검색 결과'
        return context


# 여행사 페이지
class AgencyList(ListView):
    model = TourAgency
    ordering = '-pk'
    paginate_by = 6
    template_name = 'tour/packagetour_list.html.html'
class AgencyPage(AgencyList):
    # 페이지네이션 갯수
    paginate_by = 6
    ordering = '-pk'

    # 검색 결과 반환
    def get_queryset(self):
        pk = self.kwargs['pk']
        # 해당 여행사가 작성한 모든 포스트 불러오기
        tour_list = PackageTour.objects.filter(agency=pk)
        return tour_list

    # 추가적으로 전당할 데이터
    def get_context_data(self, **kwargs):
        context = super(AgencyPage, self).get_context_data()
        pk = self.kwargs['pk']
        agency = TourAgency.objects.filter(pk=pk)
        search_info_keyword = agency[0].name
        context['search_info'] = '여행사 검색'
        context['search_info_keyword'] = search_info_keyword
        context['search_info_count'] = f'총 {self.get_queryset().count()}건의 검색 결과'
        return context


# 태그 페이지
class TagList(ListView):
    model = Tag
    ordering = '-pk'
    paginate_by = 6
    template_name = 'tour/packagetour_list.html.html'
class TagPage(TagList):
    # 페이지네이션 갯수
    paginate_by = 6
    ordering = '-pk'

    # 검색 결과 반환
    def get_queryset(self):
        slug = self.kwargs['slug']
        tag = Tag.objects.get(slug=slug)
        # 태그가 있는 모든 포스트 불러오기(다대다 관계)
        tour_list = tag.packagetour_set.all() #PackageTour.objects.filter(tags__in=[tag])
        return tour_list

    # 추가적으로 전당할 데이터
    def get_context_data(self, **kwargs):
        context = super(TagPage, self).get_context_data()
        slug = self.kwargs['slug']
        tag = Tag.objects.get(slug=slug)
        context['search_info'] = '태그 검색'
        context['search_info_keyword'] = tag.name
        context['search_info_count'] = f'총 {self.get_queryset().count()}건의 검색 결과'
        return context


# 댓글 자징하기
def create_comment(request, pk):
    # 로그인 되어져있는지
    if request.user.is_authenticated:
        # pk 포스트 가져오기
        tour = get_object_or_404(PackageTour, pk=pk)
        if request.method == "POST":
            # 댓글 내용 전달받기
            comment = Comment()
            comment.tour = tour
            comment.author = request.user
            comment.content = request.POST['comment_context']
            comment.created_at = timezone.now()
            comment.save()
            return redirect(comment.get_absolute_url())

    return redirect(tour.get_absolute_url())

# CBV 방법
# 패키지 여행 목록 페이지
class PackageTourList(ListView):
    model = PackageTour
    ordering = '-pk'
    # 페이지네이션 갯수
    paginate_by = 6
# 여행 장소 검색
class PackageTourSearchPlace(PackageTourList):
    # 페이지네이션 갯수
    paginate_by = 6

    # 검색 결과 반환
    def get_queryset(self):
        q = self.kwargs['q']
        # name과 category에 q 키워드를 가지고 있는지
        packagetour_list = PackageTour.objects.filter(
            Q(name__contains=q) | Q(category__name__contains=q)
        ).distinct() # 중복 없이
        return packagetour_list

    # 추가적으로 전당할 데이터
    def get_context_data(self, **kwargs):
        context = super(PackageTourSearchPlace, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = '여행 장소 검색'
        context['search_info_keyword'] = f'{q}'
        context['search_info_count'] = f'총 {self.get_queryset().count()}건의 검색 결과'
        return context


# 여행 날짜 검색
class PackageTourSearchDate(PackageTourList):
    # 페이지네이션 갯수
    paginate_by = 6

    # 검색 결과 반환
    def get_queryset(self):
        value = self.kwargs['value'].split('_')
        startDate = value[0]
        endDate = value[1]
        # 날짜 검색
        packagetour_list = PackageTour.objects.filter(
            start_day__range=(startDate, endDate)
        ).distinct()  # 중복 없이
        return packagetour_list

    # 추가적으로 전당할 데이터
    def get_context_data(self, **kwargs):
        context = super(PackageTourSearchDate, self).get_context_data()
        value = self.kwargs['value'].split('_')
        startDate = value[0].split('-')
        endDate = value[1].split('-')
        context['search_info'] = '여행 날짜 검색'
        context['search_info_keyword'] = f'{startDate[1]}/{startDate[2]} ~ {endDate[1]}/{endDate[2]}'
        context['search_info_count'] = f'총 {self.get_queryset().count()}건의 검색 결과'
        return context


# 여행 가격 검색
class PackageTourSearchPrice(PackageTourList):
    # 페이지네이션 갯수
    paginate_by = 6

    # 검색 결과 반환
    def get_queryset(self):
        value = self.kwargs['value'].split('_')
        minValue = value[0]
        maxValue = value[1]
        # 가격대 검색
        packagetour_list = PackageTour.objects.filter(
            price__range=(minValue, maxValue)
        ).distinct() # 중복 없이
        return packagetour_list

    # 추가적으로 전당할 데이터
    def get_context_data(self, **kwargs):
        context = super(PackageTourSearchPrice, self).get_context_data()
        value = self.kwargs['value'].split('_')
        minValue = value[0]
        maxValue = value[1]
        context['search_info'] = '여행 가격 검색'
        context['search_info_keyword'] = f'{minValue}원 ~ {maxValue}원'
        context['search_info_count'] = f'총 {self.get_queryset().count()}건의 검색 결과'
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
        # 댓글 가져오기
        context['comment_form'] = CommentForm
        return context


# 패키지 여행 수정
class PackageTourUpdate(LoginRequiredMixin, UpdateView):
    model = PackageTour
    fields = ['name', 'content', 'image', 'price', 'head_image',
              'head_text', 'start_day', 'end_day', 'category', 'agency']
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


# 댓글 수정
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'tour/comment_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        # 로그인 되어져있는지 + 로그인된 사용자와 글 작성자가 같은지
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


# 패키지 여행 생성 패아지
# 로그인 한 사람만 접근 가능 : LoginRequiredMixin
class PackageTourCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = PackageTour
    # created_at 은 자동이라 입력 X
    fields = ['name', 'content', 'image', 'price', 'head_image',
              'head_text', 'start_day', 'end_day', 'category', 'agency']

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




# 패키지 여행 삭제
class PackageTourDelete(LoginRequiredMixin, DeleteView):
    model = PackageTour
    success_url = '/tour/list'
    context_object_name = 'tour'


# 댓글 삭제
def comment_delete_redirect_to_about_me(request, author_comment):
    value = author_comment.split('_')
    author_pk = value[0]
    comment_pk = value[1]

    comment = get_object_or_404(Comment, pk=comment_pk)

    comment.delete()

    return redirect(f'/about/me/{author_pk}')

def comment_delete_redirect_to_tour_detail(request, pk_comment):
    value = pk_comment.split('_')
    tour_pk = value[0]
    comment_pk = value[1]

    comment = get_object_or_404(Comment, pk=comment_pk)

    comment.delete()

    return redirect(f'/tour/list/{tour_pk}')


# 좋아요
def like_post(request, pk):
    if request.user.is_authenticated:
        tour = get_object_or_404(PackageTour, pk=pk)
        if request.user in tour.like_users.all():
            tour.like_users.remove(request.user)
        else:
            tour.like_users.add(request.user)
        return redirect(f'/tour/list/{pk}')
    else:
        return redirect(f'/accounts/login/')


# FBV 방법
# html 어떻게 보이는지 테스트
def testTicket(request):
    return render(request, 'tour/test.html')
