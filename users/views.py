from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django import forms
from .models import CustomUser
from posts.models import Post
from django.contrib import messages

# Create your views here.
def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

@login_required
def feed_view(request):
    user = request.user

    user_blocked = request.user.blocked.values_list('id', flat=True)

    posts = Post.objects.exclude(user__in=user_blocked).order_by('-posting_date')

    user_likes = request.user.like_post.values_list('id', flat=True)
    following_users = request.user.following.values_list('id', flat=True)

    return render(request, 'feed.html', {
        'user': request.user,
        'followers': user.followers.count(),
        'following': user.following.count(),
        'posts' : posts,
        'user_likes' : user_likes,
        'following_users' : following_users
    })

def api_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            username = data.get('name')
            email = data.get('email')
            password = data.get('password')

            if CustomUser.objects.filter(name=username).exists():
                return JsonResponse({'error': 'Usuário já existe.'}, status=400)

            user = CustomUser.objects.create_user(name=username, email=email, password=password)
            user.save()

            return JsonResponse({'message': 'Usuário cadastrado com sucesso.'}, status=201)
            #return redirect('login')

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido.'}, status=405)

def api_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            password = data.get('password')
            useremail = data.get('email')

            if not useremail or not password:
                return JsonResponse({'error': 'Email e senha são obrigatórios'}, status=400)

            try:
                user_account = CustomUser.objects.get(email=useremail)
            except:
                return JsonResponse({'erro' : 'Usuario não encontrado'}, status=404)

            user = authenticate(request, username=useremail , password=password)

            if user is not None:
                login(request, user)
            else:
                return JsonResponse({'error': 'Senha incorreta.'}, status=401)
        except Exception as e:
            print(f"Erro no login: {str(e)}")
            return JsonResponse({'erro no login': str(e)}, status=500)
    
    print("Método não permitido")
    return JsonResponse({'error' : 'erro de login sem post'})

class ProfileImageForm(forms.ModelForm):

    password = forms.CharField(
        label='Nova senha',
        required=False,
        widget=forms.PasswordInput
    )

    password_confirm = forms.CharField(
        label='Confirmar nova senha',
        required=False,
        widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ['name','profile_image', 'background_image']


def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data.get("password")
    password_confirm = cleaned_data.get("password_confirm")

    if password and password != password_confirm:
        self.add_error("password_confirm", "As senhas não coincidem.")
    return cleaned_data

@login_required
def edit_perfil(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            new_password = form.cleaned_data.get('password')
            if new_password:
                user.set_password(new_password)
                user.save()

            if new_password:
                update_session_auth_hash(request, user)

            return redirect('feed')
    else:
        form = ProfileImageForm(instance=user)

    return render(request, 'user_editor.html', {'form': form})

@login_required
def follow_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if user != request.user:
        if user in request.user.following.all():
            request.user.following.remove(user)
        else:
            request.user.following.add(user)

    return redirect('feed')

@login_required
def block_user(request, user_id):
    user_block = get_object_or_404(CustomUser, id=user_id)
    request.user.blocked.add(user_block)

    request.user.following.remove(user_block)

    JsonResponse({'message' : 'O Usuário {user.block.name} foi bloqueado'})

    return redirect('feed')

def unblock_user(request, user_id):
    if request.method == "POST":
        user_block = get_object_or_404(CustomUser, id=user_id)
        request.user.blocked.remove(user_block)

    return redirect('edit')