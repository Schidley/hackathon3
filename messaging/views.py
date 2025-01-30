from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView
from .models import Post
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import CommentForm

from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import CommentForm

def home_view(request):
    interest = request.GET.get('interest')
    if interest:
        posts = Post.objects.filter(interests__icontains=interest)
    else:
        posts = Post.objects.all()

    selected_post_id = request.GET.get('post_id')
    selected_post = None
    comment_added = request.GET.get('comment_added') == 'true'
    if selected_post_id:
        selected_post = get_object_or_404(Post, id=selected_post_id)

    # Handle comment submission
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post_id = request.POST.get('post_id')
            comment.save()
            # Redirect back to home with the selected post and interest filter, if any
            redirect_url = f'{request.path}?post_id={comment.post_id}&comment_added=true'
            if interest:
                redirect_url += f'&interest={interest}'
            return redirect(redirect_url)

    else:
        form = CommentForm()

    interests = Post.objects.values_list('interests', flat=True).distinct()
    return render(request, 'messaging/home.html', {
        'posts': posts,
        'selected_interest': interest,
        'interests': interests,
        'form': form,
        'selected_post': selected_post,
        'comment_added': comment_added,
    })

@login_required
def profile_view(request):
    return render(request, 'registration/profile.html')

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')  # Redirect to the 'post_list' view
    else:
        form = PostForm()
    return render(request, 'messaging/add_post.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})



class PostListView(ListView):
    model = Post
    template_name = 'messaging/post_list.html'  # Specify your template name here
    context_object_name = 'posts'

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})
