from django.shortcuts import render, redirect, HttpResponse
from .models import Category, Tag, Blog
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authen.models import User


def home(request):
    cats = Category.objects.all()
    blog_list = Blog.objects.all()
    page_num = request.GET.get('page', 1)
    paginator = Paginator(blog_list, 5)    
    try:
        blogs = paginator.page(page_num)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {"cats":cats, "blogs": blogs})


def search_blog(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        res = Blog.objects.filter(title__icontains=content) | Blog.objects.filter(content__icontains=content)
        return render(request, 'search_result.html', {"res": res})


def user_blog_detail(request, id, pk):
    user = User.objects.get(id=id)
    blog = Blog.objects.get(create_by_id=id, id=pk)
    return render(request, 'user_blog_detail.html', {'user': user, 'blog': blog })


def filter_by_user(request, id):
    try:
        user = User.objects.get(id=id)
        blogs = Blog.objects.filter(create_by=id)
        return render(request, 'user_blog.html', {'blogs': blogs, 'user':user})
    except:
        return HttpResponse('user not found')


def my_blog_delete(request, id):
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    
    my_blog_detail = Blog.objects.get(id=id)
    if request.user != my_blog_detail.create_by:
        return HttpResponse("This blog is belong to another user")

    my_blog_detail.delete()
    return redirect('my_blog')


def my_blog_edit(request, id):
    if not request.user.is_authenticated:
        return redirect('/auth/login')

    categories = Category.objects.all()  
    tags = Tag.objects.all()  
    blog = Blog.objects.get(id=id)
    if request.user != blog.create_by:
        return HttpResponse("This blog is belong to another user")
    
    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        blog.update_on = datetime.now()
        blog.update_by = request.user
        blog.save()
        tags = request.POST.getlist('tags')
        for pk in tags:
            tag = Tag.objects.get(pk=pk)
            blog.tags.add(tag)
        return redirect('my_blog')
    return render(request, 'my_blog_edit.html', {"blog": blog, "categories": categories, 'tags': tags})


def my_blog_detail(request, id):
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    
    my_blog_detail = Blog.objects.get(id=id)
    return render(request, 'my_blog_detail.html', {"my_blog_detail": my_blog_detail})


def my_blog(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    
    my_blogs = Blog.objects.filter(create_by=request.user)
    return render(request, 'my_blog.html', {'my_blogs': my_blogs})


def blog_detail(request, id):
    try:
        blog = Blog.objects.get(id=id)
        return render(request, 'blog_detail.html', {"blog": blog})
    except:
        return HttpResponse('Blog not found')


def edit_blog(request, id):
    if not request.user.is_authenticated:
        return redirect('/auth/login')

    try:
        tags = Tag.objects.all()
        categories = Category.objects.all()
        blog = Blog.objects.get(id=id)
        if blog.create_by != request.user:
            return HttpResponse('You are not the owner')
        
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            blog.title = title
            blog.content = content
            blog.update_on = datetime.now()
            blog.update_by = request.user
            blog.save()
            tags = request.POST.getlist('tags')
            for pk in tags:
                tag = Tag.objects.get(pk=pk)
                blog.tags.add(tag)
            return redirect('/blog/categories')
        
        else:
            return render(request, 'edit_form.html', {'blog': blog, 'tags': tags, 'categories': categories})

    except:
        return HttpResponse('blog not found')


def create_blog(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    
    categories = Category.objects.all()
    all_tags = Tag.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        private = request.POST.get('private', False)
        category = request.POST.get('category')
        create_by = request.user
        blog = Blog(title=title, content=content, private=private, category_id=category, create_by=create_by)
        blog.save()
        tags = request.POST.getlist('tags')
        for id in tags:
            tag = Tag.objects.get(id=id)
            blog.tags.add(tag)
        return redirect('home')
    
    return render(request, 'new_post.html', {'categories': categories, 'all_tags': all_tags})


def delete_tag(request, id):
    if not request.user.is_authenticated:
        return redirect('/auth/login')

    tag = Tag.objects.get(id=id)
    tag.delete()


def create_tag(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login')

    if request.method == 'POST':
        name = request.POST['name']
        tags = Tag.objects.filter(name=name)
        if len(tags)>0:
            return HttpResponse('Tag existed')
        tag = Tag(name=name,create_by=request.user)
        tag.save()
        return redirect('/blog/new')
    return render(request, 'tags.html')


def category_create(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    
    if request.method == 'POST':
        name = request.POST['name']
        category = Category(name=name)
        category.save()
        return redirect('home')
    return render(request, 'new_category.html')


def category_detail(request, id):
    cats = Category.objects.all()
    cat = Category.objects.get(id=id)
    blogs = Blog.objects.filter(category=id)
    return render(request, 'category_detail.html', {'cat': cat, 'cats': cats, 'blogs': blogs})


def update_category(request, id):
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    
    try:
        cat = Category.objects.get(id=id)
        if request.method == 'POST':
            cat.name = request.POST['name']
            cat.save()

    except:
        return redirect('home')


def delete_category(request, id):
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    
    try:
        cat = Category.objects.get(id=id)
        cat.delete()
        return HttpResponse('Category removed')
    except:
        return HttpResponse('Not found')
