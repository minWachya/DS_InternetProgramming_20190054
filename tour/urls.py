from django.urls import path
from . import views

# 서버ip/tour
urlpatterns = [
    # FBV 방법
    # 서버ip/tour
    path('', views.index),
    path('test', views.index1),
]