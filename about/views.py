from django.shortcuts import render
from tour.models import Comment, Category
from django.views.generic import ListView
from django.db.models import Q

# 마이 페이지
def about_me(request):
    comment_list = Comment.objects.filter(author__username=request.user.username)

    return render(request, 'about/me.html',
                    {
                        'comment_list':comment_list,
                    },
                  )
class CommentList(ListView):
    model = Comment
    ordering = 'created_at'
    paginate_by = 6
    template_name = 'about/me.html'

# 여행 장소 검색
class MyComments(CommentList):
    # 페이지네이션 갯수
    paginate_by = 6
    ordering = 'created_at'

    # 검색 결과 반환
    def get_queryset(self):
        pk = self.kwargs['pk']
        # 작성자가 author인 댓글만 가져오기
        comment_list = Comment.objects.filter(
            Q(author__pk=pk)
        ).distinct() # 중복 없이
        return comment_list


# 회사 소개
def about_us(request):
    # 차트 데이터 : 카테고리 별 상품의 갯수

    return render(request, 'about/us.html',
                  {
                      'categories': Category.objects.all(),
                  }
                  )
