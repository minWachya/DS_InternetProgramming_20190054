from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# 서버ip/about/
urlpatterns = [
    # 마이페이지
    path('me/<int:pk>/', views.MyComments.as_view()),
    # 좋아요 목록
    path('me/like/<int:pk>/', views.MyLikes.as_view()),
    # 회사 소개 : 서버ip/tour/about_us
    path('us/', views.about_us),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)