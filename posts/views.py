from django.shortcuts import render, redirect
from .forms import PostModelForm
from .models import Post


# Create your views here.
def create(request):
    if request.method == 'POST':
        form = PostModelForm(request.POST)
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