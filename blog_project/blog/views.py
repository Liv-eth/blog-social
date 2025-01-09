from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Comment, Category, Notification
from .forms import UserRegistrationForm, PostForm, CommentForm
from .utils import create_notification  # Add this import

def home(request):
    posts = Post.objects.filter(status='published').order_by('-created_at')
    categories = Category.objects.all()
    
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    # Add unread notifications count
    unread_notifications = 0
    if request.user.is_authenticated:
        unread_notifications = request.user.notifications.filter(is_read=False).count()
    
    return render(request, 'blog/home.html', {
        'posts': posts,
        'categories': categories
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully. Welcome, {user.username}!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(active=True)
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
            # Create notification for post author
            if comment.author != post.author:  # Don't notify if commenting on own post
                create_notification(
                    recipient=post.author,
                    sender=request.user,
                    notification_type='comment',
                    post=post,
                    comment=comment
                )
            
            messages.success(request, 'Your comment has been added successfully.')
            return redirect('post_detail', pk=pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'blog/post_form.html', {
        'form': form,
        'is_edit': False
    })

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user is the author
    if post.author != request.user:
        messages.error(request, "You don't have permission to edit this post!")
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Your post has been updated successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_form.html', {
        'form': form,
        'is_edit': True
    })

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user is the author
    if post.author != request.user:
        messages.error(request, "You don't have permission to delete this post!")
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted successfully!')
        return redirect('home')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    
    # Check if user is the comment author
    if comment.author != request.user:
        messages.error(request, "You don't have permission to delete this comment!")
        return redirect('post_detail', pk=post_pk)
    
    comment.delete()
    messages.success(request, 'Your comment has been deleted successfully!')
    return redirect('post_detail', pk=post_pk)

def search(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(category__name__icontains=query),
            status='published'
        ).distinct()
    else:
        posts = []
    
    return render(request, 'blog/search_results.html', {
        'posts': posts,
        'query': query
    })

@login_required
def notifications(request):
    notifications = request.user.notifications.all()
    unread_count = notifications.filter(is_read=False).count()
    
    # Mark all as read
    if request.method == 'POST':
        notifications.update(is_read=True)
        return redirect('notifications')
    
    return render(request, 'blog/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })

@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    if notification.recipient == request.user:
        notification.is_read = True
        notification.save()
    return redirect('notifications')