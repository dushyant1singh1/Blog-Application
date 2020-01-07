from django.shortcuts import render,get_object_or_404
from .models import Post
from django.core.paginator import Paginator,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail
# Create your views here.
# def post_list(request):
#    # posts=Post.objects.filter(status="published")
#     object_list=Post.published.all()
#     paginator=Paginator(object_list,3)#3 post in each page
#     page=request.GET.get('page')
#     try:
#         posts=paginator.page(page)
#     except PageNotAnInteger:
#         #if page is not an integer deliver the first page
#         posts=paginator.page(1)
#     except EmptyPage:
#         #if pge is out of range deliver last page of results
#         posts=paginator.page(paginator.num_pages)
#     return render(request
#                         ,'blog/post/list.html'
#                         ,{'posts':posts,'page':page})

def post_detail(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='published'
                                        ,publish__year=year
                                        ,publish__month=month
                                        ,publish__day=day)
    return render(request
                        ,'blog/post/detail.html'
                        ,{'post':post})


class PostListView(ListView):
    queryset=Post.published.all()
    context_object_name='posts'
    paginate_by=2
    template_name='blog/post/list.html'

def post_share(request,post_id):
    post=get_object_or_404(Post,id=post_id,status='published')#its a shortcut to retreive the post by id 
    # I used same view for both displaying the initial form and processing the submitted data. we diffrentiate whether the form was submitted or not based
    #on the request method we assume that if we get a GET request, an empty form has to be displayed and if we get a POST request, the 
    # form is submitted and needs to be processed.
    sent=False
    if request.method=='POST':#form was submitted
        form=EmailPostForm(request.POST)
        if form.is_valid():#form validation is passed
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{}({}) recommends your reading "{}"'.format(cd['name'],cd['email'],post.title)
            message='Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title,post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'admin@myblog.com',[cd['to']])
            sent=True
    else:
        form=EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})
