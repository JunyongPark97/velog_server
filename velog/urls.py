"""velog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/list', blog_list_deprecated),

    path('blogs', blog_list_view),
    path('blog/<int:id>', blog_retrieve_view),

    path('blogs_tag', blog_list_view_with_tags),
    path('blogs_tag_v2', blog_list_view_with_tags_v2),

    path('user/<int:user_id>/blogs', blog_list_with_owner),
    path('user/<int:user_id>/blog/<int:blog_id>', blog_retrieve_with_owner),

    # DRF
    path('api/blog/<int:blog_id>', blog_retrieve_api_view),

    # CBV
    path('api/blog_v2/<int:blog_id>', BlogAPIView.as_view())
]
