from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# 서버ip/about/
urlpatterns = [
    # FBV 방법
    # 서버ip/
    path('me/', views.about_me),
    # 회사 소개 : 서버ip/tour/about_us
    path('us/', views.about_us),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)