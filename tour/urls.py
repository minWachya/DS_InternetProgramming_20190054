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
    # 패키지 투어 목록 : 서버ip/tour/list
    path('tour/list', views.PackageTourList.as_view()),
    # 패키지 투어 상세 : 서버ip/tour/pk
    path('tour/list/<int:pk>/', views.PackageTourDetail.as_view()),
    # 패키지 투어 생성
    path('tour/create_tour/', views.PackageTourCreate.as_view()),
    # 패키지 투어 수정
    path('tour/update/<int:pk>/', views.PackageTourUpdate.as_view()),

    path('tour/test', views.testTicket),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)