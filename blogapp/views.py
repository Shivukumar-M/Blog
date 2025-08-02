from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from django.http import JsonResponse
from .models import Post, Category, Tag, Comment, Newsletter, Contact
from .forms import CommentForm, NewsletterForm, ContactForm

def index(request):
    # Get featured posts (high rating or most viewed)
    featured_posts = Post.objects.filter(
        status='published',
        rating__gte=8.0
    ).order_by('-views')[:3]
    
    # Get recent posts
    recent_posts = Post.objects.filter(status='published').order_by('-created_at')[:9]
    
    # Get popular categories
    popular_categories = Category.objects.annotate(
        post_count=Count('post')
    ).filter(post_count__gt=0)[:6]
    
    context = {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'popular_categories': popular_categories,
    }
    return render(request, 'index.html', context)

def detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Increment view count
    post.increment_views()
    
    # Get related posts
    related_posts = Post.objects.filter(
        status='published',
        category=post.category
    ).exclude(id=post.id)[:4]
    
    comments = post.comments.filter(is_approved=True)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment has been submitted!')
            return redirect('detail', slug=slug)
    else:
        form = CommentForm()
    
    context = {
        'post': post,
        'form': form,
        'comments': comments,
        'related_posts': related_posts,
    }
    return render(request, 'detail.html', context)

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(
        status='published',
        category=category
    ).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'posts': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'category.html', context)

def search(request):
    query = request.GET.get('q', '')
    posts = []
    
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(anime_title_jp__icontains=query) |
            Q(studio__icontains=query) |
            Q(tags__name__icontains=query),
            status='published'
        ).distinct().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'posts': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'search.html', context)

def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            newsletter, created = Newsletter.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'Successfully subscribed to newsletter!')
            else:
                messages.info(request, 'You are already subscribed!')
        else:
            messages.error(request, 'Please enter a valid email address.')
    
    return redirect('index')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {'form': form}
    return render(request, 'contact.html', context)

def archive(request):
    # Group posts by year and month
    posts = Post.objects.filter(status='published').order_by('-created_at')
    
    # Get all categories and tags for sidebar
    categories = Category.objects.annotate(
        post_count=Count('post')
    ).filter(post_count__gt=0)
    
    tags = Tag.objects.annotate(
        post_count=Count('post')
    ).filter(post_count__gt=0)[:20]
    
    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'archive.html', context)

def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(
        status='published',
        tags=tag
    ).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'posts': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'tag.html', context)