import os

from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
# Create your views here.


# 회원가입
from django.views import View

class KakaoException(Exception):
    pass

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

# 카카오 로그인
def kakaoLoginLogic(request):
    _restApiKey = '8a338d4b56af8cd51ead20df18bfb274'
    _redirectUrl = 'http://127.0.0.1:8000/accounts/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/authorize?client_id={_restApiKey}&redirect_uri={_redirectUrl}&response_type=code'
    return redirect(_url)
def kakaoLoginLogicRedirect(request):
    _qs = request.GET['code']
    _restApiKey = '8a338d4b56af8cd51ead20df18bfb274'
    _redirect_uri = 'http://127.0.0.1:8000/accounts/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={_restApiKey}&redirect_uri={_redirect_uri}&code={_qs}'
    _res = requests.post(_url)
    _result = _res.json()
    request.session['access_token'] = _result['access_token']
    request.session.modified = True

    # 사용자 정보 받아오기
    access_token = _result['access_token']
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    kakao_account = profile_json.get("kakao_account")
    email = kakao_account.get("email")

    user = User.objects.create_user(
                username=email,
                email=email,
    )
    user.set_unusable_password()
    user.save()
    # after user is saved to db, login the user
    login(
        request,
        user,
    )

    return render(request, 'tour/index.html')

def kakao_callback(request):
    try:
        app_rest_api_key = os.environ.get("'8a338d4b56af8cd51ead20df18bfb274'")
        redirect_uri = 'http://127.0.0.1:8000/accounts/kakaoLoginLogicRedirect'
        user_token = request.GET.get("code")
        # post request
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_rest_api_key}&redirect_uri={redirect_uri}&code={user_token}"
        )

        token_response_json = token_request.json()
        error = token_response_json.get("error", None)
        # if there is an error from token_request
        if error is not None:
            raise KakaoException()
        access_token = token_response_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        # print(profile_json)
        # parsing profile json
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email", None)
        if email is None:
            raise KakaoException()
        profile = kakao_account.get("profile")
        nickname = profile.get("nickname")
        profile_image_url = profile.get("profile_image_url")
        try:
            user_in_db = User.objects.get(email=email)
            if user_in_db.register_login_method != User.kakao:
                raise KakaoException()
            else:
                login(
                    request,
                    user_in_db,
                    backend="django.contrib.auth.backends.ModelBackend",
                )
        except User.DoesNotExist:
            new_user_to_db = User.objects.create(
                username=email,
                email=email,
                first_name=nickname,
                register_login_method=User.REGISTER_LOGIN_KAKAO,
                email_confirmed=True,
            )
            # https://docs.djangoproject.com/en/3.0/ref/contrib/auth/#django.contrib.auth.models.User.set_unusable_password
            new_user_to_db.set_unusable_password()
            new_user_to_db.save()
            # after user is saved to db, login the user
            login(
                request,
                new_user_to_db,
                backend="django.contrib.auth.backends.ModelBackend",
            )
        return render(request, 'tour/index.html')
    except KakaoException:
        return render(request, 'tour/index.html')

# 카카오 로그아웃
def kakaoLogout(request):
    _token = request.session['access_token']
    _url = 'https://kapi.kakao.com/v1/user/logout'
    _header = {
      'Authorization': f'bearer {_token}'
    }
    # _url = 'https://kapi.kakao.com/v1/user/unlink'
    # _header = {
    #   'Authorization': f'bearer {_token}',
    # }
    _res = requests.post(_url, headers=_header)
    _result = _res.json()
    if _result.get('id'):
        del request.session['access_token']
        return render(request, 'loginoutSuccess.html')
    else:
        return render(request, 'logoutError.html')