"""miracbaydemir URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView, logout

from posts.views import PostCreateView, PostDetailView, PostListView, HomeListView
from django.views.generic import TemplateView, CreateView

from user_authentication.views import UserListView, UserDetailView, AuthorDetailView, signup, delete_user

urlpatterns = [

	# -------- ADMIN PAGE URL --------- #
    url(r'^admin/', admin.site.urls),

    # -------- HOME PAGE URL --------- #
    url(r'^$', HomeListView.as_view()),

    # -------- LOGIN-LOGOUT URL'S --------- #
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),

    # -------- USER_AUTHENTICATION APP URL'S --------- #
    url(r'^userlist/$', UserListView.as_view()),
    url(r'^userlist/(?P<slug>[\w-]+)/$', UserDetailView.as_view()),
    url(r'^new-user/$', signup, name='signup'),
    url(r'^delete_user/(?P<id>\d+)$', delete_user, name='get_delete'),

    # <---------------- AUTHOR URL -------------->
    url(r'^authors/(?P<username>[\w-]+)/$', AuthorDetailView.as_view(), name='author-detail'),

    # -------- POSTS APP URL'S --------- #
    url(r'^posts/create/$', PostCreateView.as_view(), name='post-create'), # ADD SLUG CONSTRAINT TO NOT CREATE 'create' SLUG
    url(r'^posts/(?P<slug>[-\w]+)/$', PostListView.as_view()),
    url(r'^posts/java/(?P<slug>[-\w]+)/$', PostDetailView.as_view()),
    url(r'^posts/python/(?P<slug>[-\w]+)/$', PostDetailView.as_view()),
    url(r'^posts/queue-models/(?P<slug>[-\w]+)$', PostDetailView.as_view()),
    url(r'^posts/production-planning/(?P<slug>[-\w]+)/$', PostDetailView.as_view()),
    url(r'^posts/machine-learning/(?P<slug>[-\w]+)/$', PostDetailView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # CHANGE IF YOU ARE LIVE
## WARNING "delete_user" is for development stage, it is CSRF vulnerable