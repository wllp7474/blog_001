from venv import logger

from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib import auth
from blog import forms, models
# from django.db.models import Count
# Create your views here.


# 注册的视图函数
def register(request):
    if request.method == "POST":
        print(request.POST)
        ret = {"status": 0, "msg": ""}
        form_obj = forms.RegForm(request.POST)
        print(request.POST)
        # 帮我做校验
        if form_obj.is_valid():

            # 校验通过，去数据库创建一个新的用户
            form_obj.cleaned_data.pop("re_password")
            models.UserInfo.objects.create_user(**form_obj.cleaned_data)
            ret["msg"] = "/index/"
            return JsonResponse(ret)
        else:
            print(form_obj.errors)
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            return JsonResponse(ret)
    # 生成一个form对象
    form_obj = forms.RegForm()
    print(form_obj.fields)
    return render(request, "register.html", {"form_obj": form_obj})

# 校验用户名是否已被注册
def check_username_exist(request):
    ret = {"status": 0, "msg": ""}
    username = request.GET.get("username")
    print(username)
    is_exist = models.UserInfo.objects.filter(username=username)
    if is_exist:
        ret["status"] = 1
        ret["msg"] = "用户名已被注册！"
    return JsonResponse(ret)


def login(request):
    # if request.is_ajax():  # 如果是AJAX请求
    if request.method == "POST":
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名和密码
        username = request.POST.get("username")
        pwd = request.POST.get("password")

            # 验证码正确
            # 利用auth模块做用户名和密码的校验
        user = auth.authenticate(username=username, password=pwd)
        if user:
            auth.login(request, user)  # 将登录用户赋值给 request.user
            ret["msg"] = "/index/"
        else:
            # 用户名密码错误
            ret["status"] = 1
            ret["msg"] = "用户名或密码错误！"
    # else:
    #     ret["status"] = 1
    #     ret["msg"] = "验证码错误"

        return JsonResponse(ret)
    return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return redirect("/index/")

def index(request):
    # 查询所有的文章列表
    article_list = models.Article.objects.all()

    return render(request, "index.html", {"article_list": article_list})


# 个人博客主页
def home(request, username, *args):
    logger.debug("home视图获取到用户名:{}".format(username))
    # 去UserInfo表里把用户对象取出来
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        logger.warning("又有人访问不存在页面了...")
        return HttpResponse("404")
    # 如果用户存在需要将TA写的所有文章找出来

    if not args:
        logger.debug("args没有接收到参数，默认走的是用户的个人博客页面！")
        # 我的文章列表
        article_list = models.Article.objects.filter(user=user)

    else:
        logger.debug(args)
        logger.debug("------------------------------")

    return render(request, "home.html", {
        "username": username,
        "article_list": article_list,
    })



def article_detail(request, username, pk):
    """
    :param username: 被访问的blog的用户名
    :param pk: 访问的文章的主键id值
    :return:
    """
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")
    # 找到当前的文章
    article_obj = models.Article.objects.filter(pk=pk).first()

    # 所有评论列表

    comment_list=models.Comment.objects.filter(article_id=pk)


    return render(
        request,
        "article_detail.html",
        {
            "username": username,
            "article": article_obj,
            "comment_list":comment_list
         }
    )




def comment(request):

    print(request.POST)

    pid=request.POST.get("pid")
    article_id=request.POST.get("article_id")
    content=request.POST.get("content")
    user_pk=request.user.pk
    response={}
    if not pid:  #根评论
        comment_obj=models.Comment.objects.create(article_id=article_id,user_id=user_pk,content=content)
    else:
        comment_obj=models.Comment.objects.create(article_id=article_id,user_id=user_pk,content=content,parent_comment_id=pid)



    response["create_time"]=comment_obj.create_time.strftime("%Y-%m-%d")
    response["content"]=comment_obj.content
    response["username"]=comment_obj.user.username

    return JsonResponse(response)




def comment_tree(request,article_id):

    ret=list(models.Comment.objects.filter(article_id=article_id).values("pk","content","parent_comment_id"))
    print(ret)
    return JsonResponse(ret,safe=False)
