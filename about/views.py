from django.shortcuts import render
from tour.models import Comment, Category
from django.db.models import Q


def about_me(request):
    comment_list = Comment.objects.filter(author__username=request.user.username)

    return render(request, 'about/me.html',
                    {
                        'comment_list':comment_list,
                    },
                  )


# 회사 소개
def about_us(request):
    # 차트 데이터 : 카테고리 별 상품의 갯수

    return render(request, 'about/us.html',
                  {
                      'categories': Category.objects.all(),
                  }
                  )
