from django.conf.urls import url
from blog import views


urlpatterns = [
    url(r"comment/",views.comment),
    # 三和一 URL

    url(r'(\w+)/article/(\d+)/$', views.article_detail),  # 文章详情  article_detail(request, xiaohei, 1)

    url(r'(\w+)', views.home),  # home(request, username)

]