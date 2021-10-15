from django.db import models


# Create your models here.

class authenticate(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username + self.password


class DB_tucao(models.Model):
    user = models.CharField(max_length=30, null=True, verbose_name='吐槽人用户名')  # 吐槽人用户名
    text = models.CharField(max_length=1000, null=True, verbose_name='吐槽内容')  # 吐槽内容
    create_time = models.DateTimeField(auto_created=True, verbose_name='创建时间')  # 创建时间

    class Meta:
        verbose_name = '吐槽内容表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.text + str(self.create_time)


class DB_home_href(models.Model):
    name = models.CharField(max_length=30, null=True)  # 超链接名字
    href = models.CharField(max_length=2000, null=True)  # 吐槽内容

    def __str__(self):
        return self.name


class DB_project(models.Model):
    name = models.CharField(max_length=100, null=True, verbose_name='项目名字')  # 项目名字
    remark = models.CharField(max_length=1000, null=True, verbose_name='项目备注')  # 项目备注
    username = models.CharField(max_length=15, null=True, verbose_name='项目创建者名字')  # 项目创建者名字
    other_user = models.CharField(max_length=100, null=True, verbose_name='项目其他创建者名字')  # 项目其他创建者名字

    class Meta:
        verbose_name = '项目表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name) + '---' + str(self.remark) + '---' + str(self.username) + '---' + str(self.other_user)


# 接口表
class DB_apis(models.Model):
    project_id = models.CharField(max_length=10, null=True)  # 项目id
    name = models.CharField(max_length=100, null=True)  # 接口名字
    api_method = models.CharField(max_length=10, null=True)  # 请求方式
    api_url = models.CharField(max_length=1000, null=True)  # url
    api_header = models.CharField(max_length=1000, null=True)  # 请求头
    api_login = models.CharField(max_length=10, null=True)  # 是否带登陆态
    api_host = models.CharField(max_length=100, null=True)  # 域名
    des = models.CharField(max_length=100, null=True)  # 描述
    body_method = models.CharField(max_length=20, null=True)  # 请求体编码格式
    api_body = models.CharField(max_length=1000, null=True)  # 请求体
    result = models.TextField(null=True)  # 返回体 因为长度巨大，所以用大文本方式存储
    sign = models.CharField(max_length=10, null=True)  # 是否验签
    file_key = models.CharField(max_length=50, null=True)  # 文件key
    file_name = models.CharField(max_length=50, null=True)  # 文件名
    public_header = models.CharField(max_length=1000, null=True)  # 全局变量-请求头
    last_body_method = models.CharField(max_length=20, null=True)  # 上次请求体编码格式
    last_api_body = models.CharField(max_length=1000, null=True)  # 上次请求体

    class Meta:
        verbose_name = '接口表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 首页调试接口log
class DB_apis_log(models.Model):
    user_id = models.CharField(max_length=10, null=True, verbose_name='所属用户id')  # 所属用户id
    api_method = models.CharField(max_length=10, null=True, verbose_name='请求方式')  # 请求方式
    api_url = models.CharField(max_length=1000, null=True, verbose_name='url')  # url
    api_header = models.CharField(max_length=1000, null=True, verbose_name='请求头')  # 请求头
    api_login = models.CharField(max_length=10, null=True, verbose_name='是否带登陆态')  # 是否带登陆态
    api_host = models.CharField(max_length=100, null=True, verbose_name='域名')  # 域名
    body_method = models.CharField(max_length=20, null=True, verbose_name='请求体编码格式')  # 请求体编码格式
    api_body = models.CharField(max_length=1000, null=True, verbose_name='请求体')  # 请求体
    sign = models.CharField(max_length=10, null=True, verbose_name='是否验签')  # 是否验签
    file_key = models.CharField(max_length=50, null=True, verbose_name='文件key')  # 文件key
    file_name = models.CharField(max_length=50, null=True, verbose_name='文件名')  # 文件名

    class Meta:
        verbose_name = '接口log表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.api_host + self.api_url


class DB_cases(models.Model):
    project_id = models.CharField(max_length=10, null=True, verbose_name='项目id')
    name = models.CharField(max_length=50, null=True, verbose_name='用例名称')

    class Meta:
        verbose_name = '用例表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class DB_step(models.Model):
    Case_id = models.CharField(max_length=10, null=True, verbose_name='所属大用例id')  # 所属大用例id
    name = models.CharField(max_length=50, null=True, verbose_name='步骤名字')  # 步骤名字
    index = models.IntegerField(null=True, verbose_name='执行步骤')  # 执行步骤
    api_method = models.CharField(max_length=10, null=True, verbose_name='请求方式')  # 请求方式
    api_url = models.CharField(max_length=1000, null=True, verbose_name='url')  # url
    api_host = models.CharField(max_length=100, null=True, verbose_name='host')  # host
    api_header = models.CharField(max_length=1000, null=True, verbose_name='请求头')  # 请求头
    api_body_method = models.CharField(max_length=10, null=True, verbose_name='请求体编码类型')  # 请求体编码类型
    api_body = models.CharField(max_length=10, null=True, verbose_name='请求体')  # 请求体
    get_path = models.CharField(max_length=500, null=True, verbose_name='提取返回值')  # 提取返回值-路径法
    get_zz = models.CharField(max_length=500, null=True, verbose_name='提取返回值-正则')  # 提取返回值-正则
    assert_zz = models.CharField(max_length=500, null=True, verbose_name='断言返回值-正则')  # 断言返回值-正则
    assert_qz = models.CharField(max_length=500, null=True, verbose_name='断言返回值-全文检索存在')  # 断言返回值-全文检索存在
    assert_path = models.CharField(max_length=500, null=True, verbose_name='断言返回值-路径法')  # 断言返回值-路径法
    mock_res = models.CharField(max_length=1000, null=True, verbose_name='mock返回值')

    class Meta:
        verbose_name = '测试用例表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class DB_project_header(models.Model):
    project_id = models.CharField(max_length=10, null=True, verbose_name='所属项目id')  # 所属项目id
    name = models.CharField(max_length=20, null=True, verbose_name='请求头变量名字')  # 请求头变量名字
    key = models.CharField(max_length=20, null=True, verbose_name='请求头header的 key')  # 请求头header的 key
    value = models.TextField(null=True, verbose_name='请求头的value，因为有可能cookie较大，达到几千字符，所以采用大文本方式存储')  # 请求头的value，因为有可能cookie较大，达到几千字符，所以采用大文本方式存储

    class Meta:
        verbose_name = '公共请求头表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
