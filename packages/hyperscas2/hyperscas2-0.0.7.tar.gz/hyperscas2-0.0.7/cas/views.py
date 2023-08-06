# -*- coding: utf-8 -*-
"""CAS login/logout replacement views"""
import uuid
import logging
import requests
import json
import simplejson
from django.core.files.storage import default_storage, FileSystemStorage
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.conf import settings as django_settings
from django.utils import translation
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import permissions
from .auth import OAuthAuthentication
from .utils import oauthLogoutUrl

logger = logging.getLogger("default")


def is_secure(request):
    return getattr(django_settings, "IS_SECURE", request.is_secure())


def logout(request):
    """登出"""
    auth.logout(request)
    logoutUrl = oauthLogoutUrl(request)
    return HttpResponseRedirect(logoutUrl)


#  hac的语言为 zh_CN, en_US, 而 Django 只识别 zh-cn, en-us, 把 Django 的语言和 hac 的语言做一个映射
LANGUAGE_MAP = {"zh-CN": "zh_CN", "en-US": "en_US"}

HAC_LANGUAGE_TO_DJANGO = {LANGUAGE_MAP[k]: k for k in LANGUAGE_MAP}


@api_view(["PUT"])
@authentication_classes([OAuthAuthentication])
@permission_classes([permissions.IsAuthenticated])
def language(request: Request):
    pk = request.user.hacId
    lang = request.data.get("language")
    # 如果请求体中的 language 无效的话, 默认取 settings.LANGUAGE_CODE 作为系统语言
    if not (lang and lang in LANGUAGE_MAP):
        lang = django_settings.LANGUAGE_CODE
    url = f"{request.domain.hac.url}/api/admin/users/{pk}/language"
    message = "操作成功"
    try:
        requestData = {"data": {"language": LANGUAGE_MAP[lang]}}
        response = requests.put(
            url, json=requestData, headers=request.domain.hac.identify,
            timeout=10
        )
        if response.status_code != 200:
            message = "操作失败"
        else:
            response = response.json()
            if response.get("code", None) != "200000":
                message = "操作失败"
    except (
            requests.exceptions.RequestException,
            json.JSONDecodeError,
            simplejson.JSONDecodeError
    ):
        message = "操作失败"
    data = {
        "message": translation.gettext(message),
        "language": lang
    }
    request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return Response(data=data, status=200)


@api_view(["GET"])
def enviroment(request: Request) -> Response:
    """enviroment 获取title，logo等配置
    """
    """获取环境配置"""
    env = request.domain.config
    try:
        resp = requests.get(
            url=f"{request.domain.hac.url}/api/sync/env",
            params={"host": request.domain.url},
            headers=request.domain.hac.identify
                    or {"identify": "URBahpGT5tYCFd0rjy2EHe1oVYX7O3hb"},
        )
        result = resp.json()
        hacEnv = result["result"] if result.get("code") == "200000" else {}
    except (
            requests.exceptions.RequestException,
            json.JSONDecodeError,
            simplejson.JSONDecodeError,
    ):
        hacEnv = {}
    env.update(hacEnv)
    return Response(data=env, status=200)


@api_view(['GET'])
@authentication_classes([OAuthAuthentication])
@permission_classes([permissions.IsAuthenticated])
def profile(request: Request) -> Response:
    url = (
        f"{request.domain.hac.url}/api/admin/users/"
        f"{request.user.hacId}/profile"
    )
    try:
        resp = requests.get(
            url=url,
            timeout=10,
            headers=request.domain.hac.identify
                    or {"identify": "URBahpGT5tYCFd0rjy2EHe1oVYX7O3hb"},
        )
        resp = resp.json()
        hacUserInfo = resp.get("result", {})
    except (
            requests.exceptions.RequestException,
            json.JSONDecodeError,
            simplejson.JSONDecodeError
    ):
        hacUserInfo = {}

    user = request.user
    data = {
        "email": user.email,
        "username": user.username,
    }
    _profile = getattr(user, "profile", None)
    if callable(_profile):
        data.update(_profile())
    data.update(hacUserInfo)
    return Response(data=data, status=200)


def settings(request: Request):
    """重定向到hac的settings"""
    redirectUrl = f'{request.domain.hac.url}/settings'
    return HttpResponseRedirect(redirectUrl)


@api_view(['POST'])
@authentication_classes([OAuthAuthentication])
@permission_classes([permissions.IsAuthenticated])
def upload(request):
    path = uuid.uuid4().hex
    myfile = request.FILES.get("file")
    storage = request.GET.get("storage", "")
    ext = ""
    storage_class = default_storage
    if not myfile:
        return Response({"file": 'required'}, status=401)
    if "." in myfile.name:
        ext = myfile.name.split(".")[-1]
    path = f"{path}.{ext}"
    if storage:
        storage_class = FileSystemStorage()
        path = myfile.name
    file = storage_class.open(path, "wb")
    file.write(myfile.read())
    file.close()
    url = storage_class.url(path)
    return Response({"file_path": path, "url": url})
