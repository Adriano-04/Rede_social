from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Post, Comment

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

def post_comments(request, post_id):
    post = Post.objects.get(id=post_id)

    comments = post.comments.select_related('user').values(
        'user__name',
        'text',
        'created'
    )

    return JsonResponse(list(comments), safe=False)

def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        text = request.POST.get('text')

        Comment.objects.create(
            post=post,
            user=request.user,
            text=text
        )
    return redirect('feed')