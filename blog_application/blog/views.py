from django.shortcuts import render, get_object_or_404, redirect 
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from datetime import datetime
from .models import Post, Comment
from .forms import PostForm, CommentForm, CustomUserCreationForm

# List posts with pagination
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'posts': posts_page})

# Display post details and comments
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

# Create a new post
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

# Edit an existing post
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# Delete a post
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        if request.method == "POST":
            post.delete()
            return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

# User signup
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_new')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})

# User login
def login_view(request):
    return render(request, 'blog/login.html')

# Profile view
@login_required
def profile(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect('profile')  # Redirect to the profile page after saving
    return render(request, 'blog/profile.html')

# Edit a comment
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect('post_detail', pk=comment.post.id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/edit_comment.html', {'form': form, 'comment': comment})

# Delete a comment
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        post_id = comment.post.id
        comment.delete()
        return redirect('post_detail', pk=post_id)
    return redirect('post_detail', pk=comment.post.id)

# User-specific posts
@login_required
def user_posts(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_date')
    return render(request, 'blog/user_posts.html', {'user_posts': user_posts})

# Pass the current year to templates
def some_view(request):
    return render(request, 'your_template.html', {'current_year': datetime.now().year})

#back btn

def previous_page_view(request):
    # Assuming the 'id' of the post is passed as a query parameter or saved somewhere in session
    post_id = request.GET.get('post_id')  # For example, pass 'post_id' in the URL
    
    if post_id:
        return redirect('post_edit', id=post_id)
    else:
        # Redirect to a fallback page or show an error
        return redirect('post_list')  # Example: redirect to post list page
