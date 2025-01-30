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
from django.contrib.auth.decorators import login_required


# home_view
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
    if request.method == 'POST' and request.POST.get('action') == 'add_comment':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post_id = request.POST.get('post_id')
            comment.save()
            # Redirect back to home with the selected post and interest filter, and indicate comment added
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
        'action': request.GET.get('action'),
    })


# Profile
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


from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect('home')

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            # Redirect to home with post_id and interest if provided
            redirect_url = f'/?post_id={comment.post.id}'
            if 'interest' in request.GET:
                redirect_url += f'&interest={request.GET["interest"]}'
            return redirect(redirect_url)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'messaging/edit_comment.html', {'form': form, 'comment': comment})



@login_required
def delete_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        post_id = comment.post.id
        if request.user == comment.author:
            comment.delete()
            # Redirect to home with post_id and interest if provided
            redirect_url = f'/?post_id={post_id}&comment_added=true&action=delete_comment'
            if 'interest' in request.GET:
                redirect_url += f'&interest={request.GET["interest"]}'
            return redirect(redirect_url)
    return HttpResponseNotAllowed(['POST'])

