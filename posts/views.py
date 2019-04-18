from django.shortcuts import render, redirect
from .forms import PostModelForm, CommentForm
from .models import Post, Comment
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def create(request):
    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:list')
        pass
    
    else:
        form = PostModelForm()
        context = {
            'form': form
        }
        return render(request, 'posts/create.html', context)
        
@login_required       
def list(request):
    # 접속한 유저가 팔로잉 한 유저들의 Post만 보여준다
    posts = Post.objects.filter(user__in=request.user.followings.values('id')).order_by('-pk')
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/list.html', context)
    

@login_required 
def delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if post.user != request.user:
        return redirect('posts:list')
        
    post.delete()
    return redirect('posts:list')
    

@login_required   
def update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if post.user != request.user:
        return redirect('posts:list')
    
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
    

@login_required
def create_comments(request, post_id):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_id
        comment.save()
        return redirect('posts:list')
    

@login_required
def like(request, post_id):
    # 특정 유저가 특정 포스트를 좋아요 할때
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)

    return redirect('posts:list')
    