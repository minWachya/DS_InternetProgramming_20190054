from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# 서버ip/
urlpatterns = [
    # FBV 방법
    # 홈 : 서버ip/
    path('', views.index),

    # 서버ip/tour/~
    # 댓글
    path('tour/list/<int:pk>/create_comment/', views.create_comment),
    # 댓글 수정
    path('tour/update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    # 댓글 삭제
    path('tour/delete_comment_1/<str:author_comment>/', views.comment_delete_redirect_to_about_me),    # 삭제 후 마이페이지로 이동
    path('tour/delete_comment_2/<str:pk_comment>/', views.comment_delete_redirect_to_tour_detail),    # 삭제 후 상세 페이지로 이동

    # 카테고리 페이지
    path('tour/category/<str:slug>', views.category_page),
    # 여행사 페이지
    path('tour/agency/<str:pk>', views.agency_page),
    # 태그 페이지
    path('tour/tag/<str:slug>', views.tag_page),

    # 패키지 투어 목록 : 서버ip/tour/list
    path('tour/list', views.PackageTourList.as_view()),
    # 패키지 투어 상세 : 서버ip/tour/pk
    path('tour/list/<int:pk>/', views.PackageTourDetail.as_view()),
    # 패키지 투어 생성
    path('tour/create_tour/', views.PackageTourCreate.as_view()),
    # 패키지 투어 수정
    path('tour/update_tour/<int:pk>/', views.PackageTourUpdate.as_view()),
    # 패키지 투어 삭제
    path('tour/delete_tour/<int:pk>/', views.PackageTourDelete.as_view()),

    # 검색
    # 여행 장소 검색
    path('tour/search/place/<str:q>/', views.PackageTourSearchPlace.as_view()),
    # 여행 날짜 검색
    path('tour/search/date/<str:value>/', views.PackageTourSearchDate.as_view()),
    # 여행 가격 검색
    path('tour/search/price/<str:value>/', views.PackageTourSearchPrice.as_view()),

    # 테스트
    path('tour/test', views.testTicket),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)