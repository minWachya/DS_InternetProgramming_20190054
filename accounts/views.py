from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
# Create your views here.


# 회원가입
def signup(request):
    if request.method == 'POST':
        # 비밀번호가 모두 일치하면
        if request.POST['password1'] == request.POST['password2']:
            # 사용자 생성
            user = User.objects.create_user(
                                            username=request.POST['username'],
                                            password=request.POST['password1'],
                                            email=request.POST['email'],)
            # 자동 로그인
            # auth.login(request, user)
            return redirect('/')    # 홈으로 이동
        return render(request, 'accounts/signup.html')
    return render(request, 'accounts/signup.html')


# 로그인
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'accounts/login.html', {'error': 'id 또는 비밀번호가 바르지 않습니다.'})
    else:
        return render(request, 'accounts/login.html')


# 로그아웃
def logout(request):
    auth.logout(request)
    return redirect('/')