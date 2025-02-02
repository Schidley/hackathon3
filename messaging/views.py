from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.views.generic import ListView
from django.contrib.auth import authenticate
from .models import Post, Comment
from .forms import CommentForm, PostForm

# post_detail
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    form = CommentForm()
    return render(request, 'messaging/post_detail.html', {'post': post, 'comments': comments, 'form': form})

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

# add_post
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Assuming the logged-in user is the author
            post.save()
            return redirect('home')  # Redirect to the home page
    else:
        form = PostForm()
    return render(request, 'messaging/add_post.html', {'form': form})


# custom_login
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

# PostListView
class PostListView(ListView):
    model = Post
    template_name = 'messaging/post_list.html'  # Specify your template name here
    context_object_name = 'posts'

# register
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

# add_comment
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import CommentForm

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)  # Redirect after successful post
    else:
        form = CommentForm()
    return render(request, 'messaging/post_detail.html', {'form': form, 'post': post})




# edit_comment
from django.shortcuts import get_object_or_404, redirect
from .models import Comment
from .forms import CommentForm

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'messaging/post_detail.html', {'form': form, 'post': comment.post})



# delete_comment
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from .models import Comment

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST' and (comment.author == request.user or request.user.is_staff):
        comment.delete()
        return redirect('post_detail', post_id=comment.post.id)
    return HttpResponseNotAllowed(['POST'])
