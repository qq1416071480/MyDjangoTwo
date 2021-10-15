import json

from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from apitest.models import *
import time
import requests
from apitest.common.handles import request_handle
import os


# Create your views here.

# def child(request, eid, oid):
#     res = child_json(eid, oid)
#     return render(request, eid, res)


# 控制不同的页面返回不同的数据：数据分发器
# def child_json(eid, oid=''):
#     res = {}
#     if eid == 'home.html':
#         data = DB_home_href.objects.all()
#         res = {"hrefs": data}
#
#     if eid == 'project_list.html':
#         data = DB_project.objects.all()
#         res = {"projects": data}
#
#     if eid == 'P_apis.html':
#         project = DB_project.objects.filter(id=oid)[0]
#         apis = DB_apis.objects.filter(project_id=oid)
#         res = {"project": project, 'apis': apis}
#
#     if eid == 'P_cases.html':
#         project = DB_project.objects.filter(id=oid)[0]
#         res = {"project": project}
#
#     if eid == 'P_project_set.html':
#         project = DB_project.objects.filter(id=oid)[0]
#         res = {"project": project}
#     return res


# 导航栏组件
@login_required
def welcome(request):
    return render(request, 'welcome.html')


# 首页
@login_required
def home(request, id=''):
    data = DB_home_href.objects.all()
    home_log = DB_apis_log.objects.filter(user_id=request.user.id)[::-1]
    if id == '':
        res = {"hrefs": data, "home_log": home_log, **glodict(request)}
    else:
        log = DB_apis_log.objects.filter(id=id)[0]
        res = {"hrefs": data, "home_log": home_log, 'log': log, **glodict(request)}
    return render(request, 'home.html', res)


def glodict(request):
    res = {'username': request.user.username, 'userimg': f'{request.user.id}.png'}
    return res


def login(request):
    return render(request, 'login.html')


def login_action(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    # user = authenticate.objects.filter(username=username, password=password)

    user = auth.authenticate(username=username, password=password)
    print(user)

    if user is not None:
        auth.login(request, user)
        request.session['user'] = username
        return HttpResponse('成功')
    else:
        return HttpResponse('失败')


def register_action(request):
    username = request.GET.get('username')
    password = request.GET.get('password')

    try:
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return HttpResponse('注册成功')
    except:
        return HttpResponse('注册失败~用户名好像已经注册过了！')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/login/')


@login_required
def api_help(request):
    res = {**glodict(request)}
    return render(request, 'help.html', res)


@login_required
def pei(request):
    tucao_text = request.GET.get('tucao_text')
    timec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(timec)
    DB_tucao.objects.create(user=request.user.username, text=tucao_text, create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    return HttpResponse('')


@login_required
def project_list(request):
    data = DB_project.objects.all()
    res = {"projects": data, **glodict(request)}
    return render(request, 'project_list.html', res)


# 删除项目
@login_required
def delete_project(request):
    id = request.GET['id']
    DB_project.objects.filter(id=id).delete()
    DB_apis.objects.filter(project_id=id).delete()  # 删除接口
    all_Case = DB_cases.objects.filter(project_id=id)
    for i in all_Case:
        DB_step.objects.filter(Case_id=i.id).delete()
        i.delete()
    return HttpResponse('')


@login_required
def add_project(request):
    project_name = request.GET.get('project_name')
    DB_project.objects.create(name=project_name, remark='', username=request.user.username, other_user='mind')
    return HttpResponse('')


@login_required
def open_apis(request, id):
    project = DB_project.objects.filter(id=id)[0]
    apis = DB_apis.objects.filter(project_id=id)
    for i in apis:
        try:
            i.short_url = i.api_url.split('?')[0][:50]
        except:
            i.short_url = ''
    res = {"project": project, 'apis': apis, **glodict(request)}
    return render(request, 'P_apis.html', res)


@login_required
def open_cases(request, id):
    project = DB_project.objects.filter(id=id)[0]
    Cases = DB_cases.objects.filter(project_id=id)
    apis = DB_apis.objects.filter(project_id=id)
    res = {"project": project, "Cases": Cases, **glodict(request), "apis": apis}
    return render(request, 'P_cases.html', res)


@login_required
def add_case(request, id):
    DB_cases.objects.create(project_id=id, name='')
    return redirect(f'/cases/{id}/')


@login_required
def del_case(request, project_id, case_id):
    DB_cases.objects.filter(id=case_id).delete()
    DB_step.objects.filter(Case_id=case_id).delete()
    return redirect(f'/cases/{project_id}/')


@login_required
def copy_case(request, project_id, case_id):
    old_case = DB_cases.objects.filter(id=case_id)[0]
    DB_cases.objects.create(project_id=old_case.project_id, name=old_case.name + '_副本')
    return redirect(f'/cases/{project_id}/')


@login_required
def get_small(request):
    case_id = request.GET['case_id']
    steps = DB_step.objects.filter(Case_id=case_id).order_by('index')
    ret = {'all_steps': list(steps.values('index', 'id', 'name'))}
    return HttpResponse(json.dumps(ret), content_type='application/json')


@login_required
def open_project_set(request, id):
    project = DB_project.objects.filter(id=id)[0]
    res = {"project": project, **glodict(request)}
    return render(request, 'P_project_set.html', res)


# 保存项目设置
@login_required
def save_project_set(request, id):
    project_id = id
    name = request.GET['name']
    remark = request.GET['remark']
    other_user = request.GET['other_user']
    DB_project.objects.filter(id=project_id).update(name=name, remark=remark, other_user=other_user)
    return HttpResponse('')


# 保存备注
@login_required
def save_bz(request):
    api_id = request.GET['api_id']
    bz_value = request.GET['bz_value']
    DB_apis.objects.filter(id=api_id).update(des=bz_value)  # 这里的des就是描述，也就是备注
    return HttpResponse('')


# 获取备注
@login_required
def get_bz(request):
    api_id = request.GET['api_id']
    bz_value = DB_apis.objects.filter(id=api_id)[0].des
    return HttpResponse(bz_value)


# 保存接口
@login_required
def Api_save(request):
    # 提取所有数据
    api_id = request.GET['api_id']
    api_name = request.GET['api_name']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    project_id = request.GET['ts_project_id']

    # 当是返回体时，则执行上次的结果
    ts_body_method = request.GET['ts_body_method']
    # 当没有请求模式时，则报错
    if ts_body_method == 'Response':
        api = DB_apis.objects.filter(id=api_id)[0]
        ts_body_method = api.last_body_method
        ts_api_body = api.last_api_body

        if ts_body_method in ['', None]:
            return HttpResponse('请先选择好请求体编码格式和请求体，再点击Send按钮发送请求！')

    else:
        ts_api_body = request.GET['ts_api_body']

    if api_id in ['', None]:
        # 新建数据
        DB_apis.objects.create(
            name=api_name,
            project_id=project_id,
            api_method=ts_method,
            api_url=ts_url,
            api_header=ts_header,
            api_host=ts_host,
            body_method=ts_body_method,
            api_body=ts_api_body
        )
        # 修改数据
    else:
        DB_apis.objects.filter(id=api_id).update(
            name=api_name,
            api_method=ts_method,
            api_url=ts_url,
            api_header=ts_header,
            api_host=ts_host,
            body_method=ts_body_method,
            api_body=ts_api_body
        )
    # 返回
    return HttpResponse('success')


# 获取接口数据
@login_required
def get_api_data(request):
    api_id = request.GET['api_id']
    api = DB_apis.objects.filter(id=api_id).values()[0]
    return HttpResponse(json.dumps(api), content_type='application/json')


# 调试层发送请求
def api_send(request):
    # 提取所有数据
    api_id = request.GET['api_id']
    api_name = request.GET['api_name']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']
    if ts_body_method == 'Response':
        api = DB_apis.objects.filter(id=api_id)[0]
        ts_body_method = api.last_body_method
        ts_api_body = api.last_api_body
        if ts_body_method in ['', 'None']:
            return HttpResponse('请先选择好请求体编码格式和请求体，再点击Send按钮发送请求！')
        else:
            ts_api_body = request.GET['ts_api_body']
            api = DB_apis.objects.filter(id=api_id)
            api.update(last_body_method=ts_body_method, last_api_body=ts_api_body)

    header = eval(ts_header)
    if isinstance(header, dict):
        header = header
    else:
        return HttpResponse('请求头不符合json格式，请重新输入！')

    # 拼接完整url
    if ts_host[-1] == '/' and ts_url[0] == '/':  # 都有/
        url = ts_host + ts_url[1:]
    elif ts_host[-1] != '/' and ts_url[0] != '/':  # 都没有/
        url = ts_host + '/' + ts_url
    else:  # 其中一个有/
        url = ts_host + ts_url
    # 当是返回体时，则执行上次的结果
    if ts_body_method == 'None':
        response = request_handle(method=ts_method, url=url, data='', headers=header, files='')
    elif ts_body_method == 'form-data':
        ts_api_body = request.GET['ts_api_body']
        files = []
        payload = {}
        for i in eval(ts_api_body):
            payload[i[0]] = i[1]
        response = request_handle(method=ts_method, url=url, data=payload, headers=header, files='')
    elif ts_body_method == 'x-www-form-urlencoded':
        ts_api_body = request.GET['ts_api_body']
        payload = {}
        for i in eval(ts_api_body):
            payload[i[0]] = i[1]
        response = request_handle(ts_method, url, payload, header, files='')
    else:
        ts_api_body = request.GET['ts_api_body']
        if ts_body_method == 'Text':
            header['Content-Type'] = 'text/plain'
        elif ts_body_method == 'JavaScript':
            header['Content-Type'] = 'text/plain'
        elif ts_body_method == 'Json':
            header['Content-Type'] = 'text/plain'
            ts_api_body = json.dumps(ts_api_body)
        elif ts_body_method == 'Html':
            header['Content-Type'] = 'text/plain'
        elif ts_body_method == 'Xml':
            header['Content-Type'] = 'text/plain'
        response = request_handle(method=ts_method, url=url, data=ts_api_body, headers=header, files='')
    # 把返回值传递给前端页面
    response.encoding = 'utf-8'
    return HttpResponse(response.text)


# 新增接口
@login_required
def project_api_add(request, Pid):
    project_id = Pid
    DB_apis.objects.create(project_id=project_id, api_method='none', api_url='')
    return redirect('/apis/%s/' % project_id)


# 删除接口
@login_required
def project_api_del(request, id):
    project_id = DB_apis.objects.filter(id=id)[0].project_id
    DB_apis.objects.filter(id=id).delete()
    return redirect('/apis/%s/' % project_id)


# 复制接口
@login_required
def copy_api(request):
    api_id = request.GET['api_id']

    # 开始复制接口
    old_api = DB_apis.objects.filter(id=api_id)[0]

    DB_apis.objects.create(project_id=old_api.project_id,
                           name=old_api.name + '_副本',
                           api_method=old_api.api_method,
                           api_url=old_api.api_url,
                           api_header=old_api.api_header,
                           api_login=old_api.api_login,
                           api_host=old_api.api_host,
                           des=old_api.des,
                           body_method=old_api.body_method,
                           api_body=old_api.api_body,
                           result=old_api.result,
                           sign=old_api.sign,
                           file_key=old_api.file_key,
                           file_name=old_api.file_name,
                           public_header=old_api.public_header,
                           last_body_method=old_api.last_body_method,
                           last_api_body=old_api.last_api_body
                           )
    # 返回
    return HttpResponse('')


# 异常值发送请求
@login_required
def error_request(request):
    api_id = request.GET['api_id']
    new_body = request.GET['new_body']
    span_text = request.GET['span_text']
    print('----------------------------')
    print(new_body)
    print('----------------------------')
    api = DB_apis.objects.filter(id=api_id)[0]
    method = api.api_method
    url = api.api_url
    host = api.api_host
    header = api.api_header
    body_method = api.body_method
    header = json.loads(header)
    if host[-1] == '/' and url[0] == '/':  # 都有/
        url = host[:-1] + url
    elif host[-1] != '/' and url[0] != '/':  # 都没有/
        url = host + '/' + url
    else:  # 肯定有一个有/
        url = host + url
    try:
        if body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(new_body):
                payload[i[0]] = i[1]
            response = request_handle(method=method, url=url, data=payload, headers=header, files='')
        elif body_method == 'x-www-form-urlencoded':
            payload = {}
            for i in eval(new_body):
                payload[i[0]] = i[1]
            response = request_handle(method=method, url=url, data=payload, headers=header, files='')
        elif body_method == 'Json':
            header['Content-Type'] = 'text/plain'
            response = request_handle(method=method, url=url, data=new_body, headers=header, files='')
        else:
            return HttpResponse('非法的请求体类型')
        # 把返回值传递给前端页面
        response.encoding = "utf-8"
        res_json = {"response": response.text, "span_text": span_text}
        return HttpResponse(json.dumps(res_json), content_type='application/json')

    except Exception as e:
        print(e)
        res_json = {"response": '对不起，接口未通！', "span_text": span_text}
        return HttpResponse(json.dumps(res_json), content_type='application/json')


# 首页发送请求
@login_required
def Api_send_home(request):
    # 提取所有数据
    print('qwe')
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']
    ts_api_body = request.GET['ts_api_body']
    # 发送请求获取返回值
    header = eval(ts_header)
    if isinstance(header, dict):
        header = header
    else:
        return HttpResponse('请求头不符合json格式，请重新输入！')

    # 写入到数据库请求记录表中
    DB_apis_log.objects.create(user_id=request.user.id,
                               api_method=ts_method,
                               api_url=ts_url,
                               api_header=ts_header,
                               api_host=ts_host,
                               body_method=ts_body_method,
                               api_body=ts_api_body
                               )
    # 拼接完整url
    if ts_host[-1] == '/' and ts_url[0] == '/':  # 都有/
        url = ts_host[:-1] + ts_url
    elif ts_host[-1] != '/' and ts_url[0] != '/':  # 都没有/
        url = ts_host + '/' + ts_url
    else:  # 肯定有一个有/
        url = ts_host + ts_url
    try:
        if ts_body_method == 'none':
            response = requests.request(ts_method.upper(), url, headers=header, data={})

        elif ts_body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(ts_api_body):
                payload[i[0]] = i[1]
            response = requests.request(ts_method.upper(), url, headers=header, data=payload, files=files)

        elif ts_body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(ts_api_body):
                payload[i[0]] = i[1]
            response = requests.request(ts_method.upper(), url, headers=header, data=payload)

        else:  # 这时肯定是raw的五个子选项：
            if ts_body_method == 'Text':
                header['Content-Type'] = 'text/plain'
            if ts_body_method == 'JavaScript':
                header['Content-Type'] = 'text/plain'
            if ts_body_method == 'Json':
                header['Content-Type'] = 'text/plain'
            if ts_body_method == 'Html':
                header['Content-Type'] = 'text/plain'
            if ts_body_method == 'Xml':
                header['Content-Type'] = 'text/plain'
            response = requests.request(ts_method.upper(), url, headers=header, data=ts_api_body.encode('utf-8'))

        # 把返回值传递给前端页面
        response.encoding = "utf-8"
        return HttpResponse(response.text)
    except Exception as e:
        return HttpResponse(str(e))


@login_required
def get_home_log(request):
    user_id = request.user.id
    all_logs = DB_apis_log.objects.filter(user_id=user_id)
    ret = {"all_logs": list(all_logs.values("id", "api_method", "api_host", "api_url"))[::-1]}
    return HttpResponse(json.dumps(ret), content_type='application/json')


@login_required
def get_api_log_home(request):
    log_id = request.GET['log_id']
    log = DB_apis_log.objects.filter(id=log_id)
    ret = {'log': list(log.values())[0]}
    print(ret)
    return HttpResponse(json.dumps(ret), content_type='application/json')


# 上传用户头像
@login_required
def user_upload(request):
    file = request.FILES.get("fileUpload", None)  # 靠name获取上传的文件，如果没有，避免报错，设置成None
    if not file:
        return redirect('/home/')  # 如果没有则返回到首页
    new_name = str(request.user.id) + '.png'  # 设置好这个新图片的名字
    with open("apitest/static/user_img/" + new_name, 'wb+') as destination:
        for chunk in file.chunks():  # 分块写入文件
            destination.write(chunk)
    return redirect('/home/')  # 返回到首页


def add_new_step(request):
    Case_id = request.GET['Case_id']
    all_len = len(DB_step.objects.filter(Case_id=Case_id))
    DB_step.objects.create(Case_id=Case_id, name='我是新步骤', index=all_len + 1)
    return HttpResponse('')


def delete_step(request, id):
    step = DB_step.objects.filter(id=id)[0]
    index = step.index
    Case_id = step.Case_id
    step.delete()

    for i in DB_step.objects.filter(Case_id=Case_id).filter(index__gt=index):  # 遍历大于目标id的所有数据，并减1
        i.index -= 1
        i.save()
    return HttpResponse('')


def get_step(request):
    step_id = request.GET['step_id']
    step = DB_step.objects.filter(id=step_id)
    steplist = list(step.values())[0]
    return HttpResponse(json.dumps(steplist), content_type='application/json')


# 保存小步骤
def save_step(request):
    step_id = request.GET['step_id']
    name = request.GET['name']
    index = request.GET['index']
    step_method = request.GET['step_method']
    step_url = request.GET['step_url']
    step_host = request.GET['step_host']
    step_header = request.GET['step_header']
    mock_res = request.GET['mock_res']
    step_body_method = request.GET['step_body_method']
    step_api_body = request.GET['step_api_body']

    get_path = request.GET['get_path']
    get_zz = request.GET['get_zz']
    assert_zz = request.GET['assert_zz']
    assert_qz = request.GET['assert_qz']
    assert_path = request.GET['assert_path']

    DB_step.objects.filter(id=step_id).update(name=name,
                                              index=index,
                                              api_method=step_method,
                                              api_url=step_url,
                                              api_host=step_host,
                                              api_header=step_header,
                                              mock_res=mock_res,
                                              api_body_method=step_body_method,
                                              api_body=step_api_body,

                                              get_path=get_path,
                                              get_zz=get_zz,
                                              assert_zz=assert_zz,
                                              assert_qz=assert_qz,
                                              assert_path=assert_path,

                                              )
    return HttpResponse('')

def step_get_api(request):
    api_id = request.GET['api_id']
    api = DB_apis.objects.filter(id=api_id).values()[0]
    return HttpResponse(json.dumps(api), content_type='application/json')

def Run_Case(request):
    Case_id = request.GET['Case_id']
    Case = DB_cases.objects.filter(id=Case_id)[0]
    steps = DB_step.objects.filter(Case_id=Case_id)
    from apitest.run_case import run
    run(Case_id, Case.name, steps)
    return HttpResponse('')

def look_report(request, id):
    Case_id=id
    return render(request, f'Reports/{Case_id}.html')
    # return redirect(f'/static/allure-report/{id}/index.html')
