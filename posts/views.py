from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Post

# Create your views here.
def create_post(request):
    return render(request, 'create_post.html')

def create_post_view(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        image = request.FILES.get('image')

        post = Post.objects.create(
            user = request.user,
            text = text,
            image = image
        )
        return redirect('feed')
    return redirect('create_post')

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    liked = False
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count()
    })