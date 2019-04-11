from django.shortcuts import render, redirect
from .forms import PostModelForm
from .models import Post


# Create your views here.
def create(request):
    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
        pass
    
    else:
        form = PostModelForm()
        context = {
            'form': form
        }
        return render(request, 'posts/create.html', context)
        
        
def list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'posts/list.html', context)
    
    
def delete(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    return redirect('posts:list')
    
    
def update(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
    
    else:
        form = PostModelForm(instance=post)
        context = {
            'form': form
        }
        return render(request, 'posts/update.html', context)
    
    
    
    