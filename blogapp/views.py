from django.shortcuts import render, redirect ,get_object_or_404
from.models import Post
from.forms import CommentForm

def index(req):
    posts=Post.objects.all()

    return render(req, 'index.html',{
        "posts":posts
    })

def detail(req, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()  
    if req.method == 'POST':
        form = CommentForm(req.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('detail', slug=slug)
    else:
        form = CommentForm()

    return render(req, 'detail.html', {
        "post": post,
        "form": form,
        "comments": comments  
    })
