from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# 서버ip/
urlpatterns = [
    # FBV 방법
    # 홈 : 서버ip/
    path('', views.index),
    # 댓글
    path('tour/list/<int:pk>/new_comment/', views.new_comment),
    # 회사 소개 : 서버ip/tour/about_us
    path('tour/about_us', views.about_us),
    # 카테고리 페이지
    path('tour/category/<str:slug>', views.category_page),

    # 서버ip/tour/~
    # 패키지 투어 목록 : 서버ip/tour/list
    path('tour/list', views.PackageTourList.as_view()),
    # 패키지 투어 상세 : 서버ip/tour/pk
    path('tour/list/<int:pk>/', views.PackageTourDetail.as_view()),
    # 패키지 투어 생성
    path('tour/create_tour/', views.PackageTourCreate.as_view()),
    # 패키지 투어 수정
    path('tour/update/<int:pk>/', views.PackageTourUpdate.as_view()),

    # 테스트
    path('tour/test', views.testTicket),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)