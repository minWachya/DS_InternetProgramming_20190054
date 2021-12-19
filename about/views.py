from django.shortcuts import render
from tour.models import Comment, Category, TourAgency, PackageTour
from django.views.generic import ListView
from django.db.models import Q

# 마이 페이지
class CommentList(ListView):
    model = Comment
    ordering = '-pk'
    paginate_by = 6
    template_name = 'about/me.html'

# 사용자가 작성한 댓글만 반환
class MyComments(CommentList):
    # 페이지네이션 갯수
    paginate_by = 6
    ordering = '-pk'

    # 검색 결과 반환
    def get_queryset(self):
        pk = self.kwargs['pk']
        # 작성자가 author인 댓글만 가져오기
        comment_list = Comment.objects.filter(
            Q(author__pk=pk)
        ).distinct().order_by('-pk') # 중복 없이
        return comment_list

    # 추가적으로 전달할 데이터
    def get_context_data(self, **kwargs):
        context = super(MyComments, self).get_context_data()
        pk = self.kwargs['pk']

        tour_list = PackageTour.objects.filter(like_users__in=[pk])
        context['packagetour_list'] = tour_list
        return context

# 사용자가 좋아오 누른 글 반환
class PackageTourList(ListView):
    model = PackageTour
    ordering = '-pk'
    # 페이지네이션 갯수
    paginate_by = 6
    template_name = 'about/like_tours.html'
class MyLikes(PackageTourList):
    # 페이지네이션 갯수
    paginate_by = 6
    ordering = '-pk'

    # 검색 결과 반환
    def get_queryset(self):
        pk = self.kwargs['pk']
        tour_list = PackageTour.objects.filter(like_users__in=[pk])
        return tour_list

# 회사 소개
def about_us(request):
    # 차트 데이터 : 카테고리 별 상품의 갯수

    return render(request, 'about/us.html',
                  {
                      'categories': Category.objects.all(),
                      'agencies':TourAgency.objects.all(),
                  }
                  )
