from django.shortcuts import render, redirect
from .forms import PostModelForm


# Create your views here.
def create(request):
    if request.method == 'POST':
        form = PostModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:create')
        pass
    
    else:
        form = PostModelForm()
        context = {
            'form': form
        }
        return render(request, 'posts/create.html', context)