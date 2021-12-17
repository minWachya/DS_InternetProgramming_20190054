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

    # 카카오 간편 로그인
    path('kakaoLoginLogic/', views.kakaoLoginLogic),
    path('kakaoLoginLogicRedirect/', views.kakaoLoginLogicRedirect),
    path('kakaoLogout/', views.kakaoLogout),

    # 12-17 재시도
    path("login/github/", views.github_login),
    path("login/github/callback/", views.github_login_callback),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)