# encoding:utf-8

from django.views.generic import View
from Video_app.lib.base_render import render_to_response
from django.shortcuts import redirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator  # 分页


class Login(View):
    TEMPLATES = 'dashboard/auth/Login.html'

    def get(self, request):
        if request.user.is_authenticated:
            print("已经登录")
            return redirect(reverse('index'))

        data = {'error': ''}
        return render_to_response(request, self.TEMPLATES, data=data)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        data = {}
        exists = User.objects.filter(username=username).exists()
        data['error'] = '该用户不存在'
        if not exists:
            return render_to_response(request, self.TEMPLATES, data)

        user = authenticate(username=username, password=password)

        if not user:
            data['error'] = '密码错误'
            return render_to_response(request, self.TEMPLATES, data=data)

        if not user.is_superuser:
            data['error'] = '您没有权限登录'
            return render_to_response(request, self.TEMPLATES, data=data)

        login(request, user)
        return redirect('index')


class LoginOut(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('login'))


class AdminManager(View):
    TEMPLATES = 'dashboard/auth/admin.html'

    def get(self, request):
        data = {}
        users = User.objects.all()
        page = request.GET.get('page', 1)
        p = Paginator(users, 1)  # 分页
        total_pages = p.num_pages       # 获取总页数

        if int(page) <= 1:
            page = 1
        current_page = p.get_page(int(page)).object_list      # ？

        data = {'users': current_page, 'total_pages': int(total_pages), 'page_num': int(page)}
        return render_to_response(request, self.TEMPLATES, data)


class AminManagerUpdateStatus(View):
    """待修改"""

    def get(self, request):
        status = request.GET.get('status', 'on')
        _status = True if status == 'on' else False

        user_id = request.GET.get('user_id')
        user = User.objects.filter(id=user_id)
        user.update(is_superuser=_status)
        return redirect(reverse('manager'))

