from django.shortcuts import render
from rest_framework import status
from blog.models import Post
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
import json
from blog.serializers import *
# Create your views here.


def blog_list_deprecated(request):
    # Deprecated
    if request.method == "GET":
        queryset = Post.objects.all()
        # serializer = BlogListSerializer(queryset, many=True)
        temp_list = []
        
        for i in queryset:
            dic = {}
            dic["id"] = i.id
            dic["title"] = i.title
            dic["contents"] = i.contents
            temp_list.append(dic) # TODO : serialzer !!

        return HttpResponse(temp_list)


def blog_list_view(request):
    # 등록된 모든 블로그 글을 조회
    # api : /blogs
    if request.method == "GET":
        queryset = Post.objects.all()
        serializer = BlogSerializer(queryset, many=True)
        data = json.dumps(serializer.data, ensure_ascii=False) # ensure_ascii=False : json화 시킬때 한글이 유니코드화 되는 것 방지
        return HttpResponse(data)
    # POST method 의 경우. 403 Forbidden


def blog_retrieve_view(request, **kwargs):
    # 등록된 블로그의 id로 조회
    # api : /blog/<id>
    if request.method == "GET":
        blog_id = kwargs['id']
        queryset = Post.objects.all()
        blog_obj = queryset.get(id=blog_id) # TODO : 에러처리
        serializer = BlogSerializer(blog_obj)
        data = json.dumps(serializer.data, ensure_ascii=False)
        return HttpResponse(data)


def blog_list_view_with_tags(request):
    # 태그와 함께 등록된 모든 블로그 글을 조회
    # api : /blogs
    if request.method == "GET":
        queryset = Post.objects.all()
        serializer = BlogSerializerWithTags(queryset, many=True)
        data = json.dumps(serializer.data, ensure_ascii=False) # ensure_ascii=False : json화 시킬때 한글이 유니코드화 되는 것 방지
        return HttpResponse(data)
    # POST method 의 경우. 403 Forbidden


def blog_list_view_with_tags_v2(request):
    # 태크와 함께 등록된 모든 블로그 글을 조회 v2
    # api : /blogs
    if request.method == "GET":
        queryset = Post.objects.all()
        serializer = BlogSerializerWithTagsV2(queryset, many=True)
        data = json.dumps(serializer.data, ensure_ascii=False) # ensure_ascii=False : json화 시킬때 한글이 유니코드화 되는 것 방지
        return HttpResponse(data)
    # POST method 의 경우. 403 Forbidden



def blog_list_with_owner(request, **kwargs):
    # 유저의 글 조회
    # api : user/<user_id>/blogs
    if request.method == "GET":
        queryset = Post.objects.all()
        user_id = kwargs['user_id']
        print(user_id)
        blog_queryset = queryset.filter(owner_id=user_id)
        serializer = BlogSerializerWithTagsV2(blog_queryset, many=True)
        data = json.dumps(serializer.data, ensure_ascii=False) # ensure_ascii=False : json화 시킬때 한글이 유니코드화 되는 것 방지
        return HttpResponse(data)
    
def blog_retrieve_with_owner(request, **kwargs):
    # 유저의 글 조회
    # api : user/<user_id>/blog/<blog_id>
    # 굳이? blog_retrieve_view로 사용가능!
    if request.method == "GET":
        queryset = Post.objects.all()
        user_id = kwargs['user_id']
        blog_queryset = queryset.filter(owner_id=user_id)

        blog_id = kwargs['blog_id']
        blog_obj = blog_queryset.get(id=blog_id)
        serializer = BlogSerializerWithTagsV2(blog_obj)
        data = json.dumps(serializer.data, ensure_ascii=False) # ensure_ascii=False : json화 시킬때 한글이 유니코드화 되는 것 방지
        return HttpResponse(data)


# DRF 사용하여 함수형 뷰 만들기
# DRF 에선, 일일이 Json화 시키지 않아도 됨 + DRF 자체제공 폼이 있음

from rest_framework.decorators import api_view

@api_view(['GET'])
def blog_retrieve_api_view(request, blog_id): # url 에서 선언한 변수
    # blog글 1개 조회
    # api : api/blog/<blog_id>
    try:
        blog = Post.objects.get(id=blog_id)
    except Post.DoesNotExist:
        return Response({"error": {
            "code": 404,
            "message": "Blog not found!"
        }}, status=status.HTTP_404_NOT_FOUND)

    print(blog_id)
    blog = Post.objects.get(id=blog_id)
    serializer = BlogSerializerWithTagsV2(blog)
    return Response(serializer.data)
 

 # DRF class 형 뷰
 # if method= GET ~~ 쓰지 않고, 함수로 사용 가능
from rest_framework.views import APIView

class BlogAPIView(APIView):
    # 하나의 url 에 대해서 다른 메서드로 처리 가능
    """
    CBV(Class based View)의 장점
        GET, POST 등 HTTP 메소드에 따른 처리 코드를 작성할 때 if 함수 대신에 메소드 명으로 코드의 구조가 깔끔하다.
        다중상속 같은 객체지향 기법을 활용해 제너릭 뷰, 믹스인 클래스 등을 사용해 코드의 재사용과 개발 생산성을 높여준다.   
    
    /blog/ 에 대한 CBV
        get : 포스팅 목록
        post : 새 포스팅 생성
    /blog/<int:blog_id>/ 에 대한 CBV
        get : pk 번 포스팅 내용
        put : pk번 포스팅 수정
        delete : pk번 포스팅 삭제
    """

    def get_object(self, pk):
        try:
            blog = Post.objects.get(id=pk)
            return blog
        except Post.DoesNotExist:
            return Response({"error": {
                "code": 404,
                "message": "Blog not found!"
            }}, status=status.HTTP_404_NOT_FOUND)

    
    def get(self, request, blog_id):
        blog = self.get_object(blog_id) # 클래스 내부에서 공용 사용 가능한 함수
        serializer = BlogSerializerWithTagsV2(blog)
        return Response(serializer.data)
    
    def post(self, request, blog_id):
        pass



####################

# Generic View!

