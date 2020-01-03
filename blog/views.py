from django.shortcuts import render,get_object_or_404
from .models import Post
from django.core.paginator import Paginator,PageNotAnInteger
# Create your views here.
def post_list(request):
   # posts=Post.objects.filter(status="published")
    object_list=Post.published.all()
    paginator=Paginator(object_list,2)#3 post in each page
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer deliver the first page
        posts=paginator.page(1)
    except EmptyPage:
        #if pge is out of range deliver last page of results
        posts=paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'posts':posts,'page':page})

def post_detail(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='published'
                                        ,publish__year=year
                                        ,publish__month=month
                                        ,publish__day=day)
    return render(request,'blog/post/detail.html',{'post':post})
