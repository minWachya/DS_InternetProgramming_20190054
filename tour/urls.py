from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# 서버ip/tour
urlpatterns = [
    # FBV 방법
    # 홈 : 서버ip/tour
    path('', views.index),
    # 패키지 투어 목록 : 서버ip/tour/list
    path('list', views.PackageTourList.as_view()),
    # 패키지 투어 상세 : 서버ip/tour/pk
    path('list/<int:pk>/', views.PackageTourDetail.as_view()),

    path('test', views.testTicket),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)