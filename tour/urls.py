from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# 서버ip/tour
urlpatterns = [
    # FBV 방법
    # 서버ip/tour
    path('', views.index),
    path('test', views.PackageTourList.as_view()),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)