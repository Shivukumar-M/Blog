from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib.auth import login, logout
from mongoengine import NotUniqueError, DoesNotExist
from .models import Post, Category, Tag, Comment, Newsletter, Contact
from .forms import CommentForm, NewsletterForm, ContactForm, PostForm, SignUpForm


def index(request):
    # Get featured posts (high rating or most viewed)
    featured_posts = Post.objects(
        status='published',
        rating__gte=8.0
    ).order_by('-views')[:3]
    
    # Get recent posts
    recent_posts = Post.objects(status='published').order_by('-created_at')[:9]
    
    # Get popular categories with post counts
    popular_categories = []
    for category in Category.objects():
        post_count = Post.objects(category=category, status='published').count()
        if post_count > 0:
            popular_categories.append({
                'category': category,
                'post_count': post_count
            })
    popular_categories = popular_categories[:6]
    
    context = {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'popular_categories': popular_categories,
    }
    return render(request, 'index.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author_id = request.user.id
            post.author_username = request.user.username
            
            # Generate slug from title
            post.slug = slugify(post.title)
            
            # Make slug unique if it already exists
            original_slug = post.slug
            counter = 1
            while Post.objects(slug=post.slug).first():
                post.slug = f"{original_slug}-{counter}"
                counter += 1
            
            # Handle status from form submission
            if 'status' in request.POST:
                post.status = request.POST['status']
            else:
                post.status = 'published'
            
            post.save()
            
            if post.status == 'published':
                messages.success(request, f'Your post "{post.title}" has been published successfully!')
                return redirect('detail', slug=post.slug)
            else:
                messages.success(request, f'Your post "{post.title}" has been saved as draft!')
                return redirect('create_post')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PostForm()
    
    context = {
        'form': form,
    }
    return render(request, 'create_post.html', context)


def about(request):
    return render(request, "about.html")


def detail(request, slug):
    try:
        post = Post.objects(slug=slug, status='published').first()
        if not post:
            raise Post.DoesNotExist
    except Post.DoesNotExist:
        raise Http404("Post not found")
    
    # Increment view count
    post.increment_views()
    
    # Get related posts
    related_posts = Post.objects(
        status='published',
        category=post.category
    ).exclude('id', post.id)[:4] if post.category else []
    
    comments = post.get_comments()
    
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
    try:
        category = Category.objects(slug=slug).first()
        if not category:
            raise Category.DoesNotExist
    except Category.DoesNotExist:
        raise Http404("Category not found")
    
    posts = Post.objects(
        status='published',
        category=category
    ).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(list(posts), 9)
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
        # MongoEngine supports case-insensitive search
        posts = Post.objects(
            status='published'
        ).filter(
            title__icontains=query
        ) | Post.objects(
            status='published'
        ).filter(
            content__icontains=query
        ) | Post.objects(
            status='published'
        ).filter(
            anime_title_jp__icontains=query
        ) | Post.objects(
            status='published'
        ).filter(
            studio__icontains=query
        )
        
        # Remove duplicates and sort
        unique_ids = set()
        unique_posts = []
        for post in posts.order_by('-created_at'):
            if str(post.id) not in unique_ids:
                unique_ids.add(str(post.id))
                unique_posts.append(post)
        posts = unique_posts
    
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
            try:
                newsletter = Newsletter.objects(email=email).first()
                if not newsletter:
                    newsletter = Newsletter(email=email)
                    newsletter.save()
                    messages.success(request, 'Successfully subscribed to newsletter!')
                else:
                    messages.info(request, 'You are already subscribed!')
            except Exception as e:
                messages.error(request, 'Error processing subscription. Please try again.')
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
    # Get all published posts
    posts = Post.objects(status='published').order_by('-created_at')
    
    # Get all categories and tags with post counts
    categories = []
    for category in Category.objects():
        post_count = Post.objects(category=category, status='published').count()
        if post_count > 0:
            categories.append({
                'category': category,
                'post_count': post_count
            })
    
    tags = []
    for tag in Tag.objects().order_by('name'):
        post_count = Post.objects(tags=tag, status='published').count()
        if post_count > 0:
            tags.append({
                'tag': tag,
                'post_count': post_count
            })
    tags = tags[:20]
    
    # Pagination
    paginator = Paginator(list(posts), 12)
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
    try:
        tag = Tag.objects(slug=slug).first()
        if not tag:
            raise Tag.DoesNotExist
    except Tag.DoesNotExist:
        raise Http404("Tag not found")
    
    posts = Post.objects(
        status='published',
        tags=tag
    ).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(list(posts), 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'posts': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'tag.html', context)


# Sign up
def signup(req):
    if req.method == 'POST':
        form = SignUpForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            return redirect('/')
    else:
        form = SignUpForm()
    
    return render(req, 'signup.html', {'form': form})


# Logout
def logout_view(request):
    logout(request)
    return redirect('/') 