from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# 서버ip/accounts/
urlpatterns = [
    # 회원가입
    path('signup/', views.signup),
    # 로그인
    path('login/', views.login),
    # 로그아웃
    path('logout/', views.logout),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)