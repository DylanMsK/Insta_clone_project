from django.shortcuts import render
from .forms import PostModelForm


# Create your views here.
def create(request):
    if request.method == 'POST':
        pass
    
    else:
        form = PostModelForm()
        context = {
            'form': form
        }
        return render(request, 'posts/create.html', context)