from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# 서버ip/
urlpatterns = [
    # FBV 방법
    # 서버ip/
    # path('my_page', views.index),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)