"""my_ip_proj_20190054 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # 서버ip/tour/~
    path('tour/', include('tour.urls')),

    # 서버ip/my_page/~
    path('my_page/', include('my_page.urls')),

    # 마크다운
    path('markdownx/', include('markdownx.urls')),
]
# ip 주소 외 이미지 접근하려는 선언 추가
# 서버IP/media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
