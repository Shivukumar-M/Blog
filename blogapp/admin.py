from django import forms
from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.text import slugify

from .models import Category, Post


# =========================
# 🔹 FORMS
# =========================

class CategoryAdminForm(forms.Form):
    name = forms.CharField(max_length=100)
    slug = forms.CharField(max_length=120, required=False)
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))
    color = forms.CharField(max_length=7, required=False, initial="#6366f1")

    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip()
        return slugify(slug) if slug else ""


class PostAdminForm(forms.Form):
    title = forms.CharField(max_length=255)
    excerpt = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 8}))
    status = forms.ChoiceField(choices=Post.STATUS_CHOICES, initial="published")
    category = forms.ChoiceField(required=False)
    anime_type = forms.ChoiceField(choices=[("", "---------")] + Post.ANIME_TYPES, required=False)
    rating = forms.FloatField(required=False, min_value=0, max_value=10)
    episode_count = forms.IntegerField(required=False)
    release_year = forms.IntegerField(required=False)
    studio = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].choices = [("", "---------")] + [
            (str(c.id), c.name) for c in Category.objects.order_by("name")
        ]


# =========================
# 🔹 HELPERS
# =========================

def _get_category(category_id):
    if not category_id:
        return None
    try:
        return Category.objects(id=category_id).first()
    except:
        return None


def _check_admin(request):
    if not request.user.is_superuser:
        messages.error(request, "Not authorized")
        return False
    return True


# =========================
# 🔹 DASHBOARD
# =========================

def admin_dashboard(request):
    context = {
        **admin.site.each_context(request),
        "post_count": Post.objects.count(),
        "published_count": Post.objects(status="published").count(),
        "draft_count": Post.objects(status="draft").count(),
        "category_count": Category.objects.count(),
        "recent_posts": Post.objects.order_by("-created_at")[:10],
    }
    return render(request, "admin/blogapp/dashboard.html", context)


# =========================
# 🔹 CATEGORY MANAGEMENT
# =========================

def category_manager(request):
    if request.method == "POST":
        form = CategoryAdminForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            slug = form.cleaned_data["slug"] or slugify(name)

            if Category.objects(slug=slug).first():
                form.add_error("slug", "Slug already exists")
            elif Category.objects(name=name).first():
                form.add_error("name", "Category already exists")
            else:
                Category(
                    name=name,
                    slug=slug,
                    description=form.cleaned_data.get("description", ""),
                    color=form.cleaned_data.get("color") or "#6366f1",
                ).save()
                messages.success(request, f"{name} created")
                return redirect("admin:blogapp_category_manager")
    else:
        form = CategoryAdminForm()

    context = {
        **admin.site.each_context(request),
        "form": form,
        "categories": Category.objects.order_by("name"),
    }
    return render(request, "admin/blogapp/category_manager.html", context)


def delete_category(request, category_id):
    if not _check_admin(request):
        return redirect("admin:index")

    category = _get_category(category_id)
    if not category:
        messages.error(request, "Not found")
        return redirect("admin:blogapp_category_manager")

    if Post.objects(category=category).count() > 0:
        messages.error(request, "Category has posts")
        return redirect("admin:blogapp_category_manager")

    category.delete()
    messages.success(request, "Deleted successfully")
    return redirect("admin:blogapp_category_manager")


def seed_default_categories(request):
    if not _check_admin(request):
        return redirect("admin:index")

    defaults = ["Blog", "News", "Review"]
    for name in defaults:
        slug = slugify(name)
        if not Category.objects(slug=slug).first():
            Category(name=name, slug=slug).save()

    messages.success(request, "Default categories added")
    return redirect("admin:blogapp_category_manager")


# =========================
# 🔹 POST MANAGEMENT
# =========================

def post_manager(request):
    if request.method == "POST":
        form = PostAdminForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            category = _get_category(data.get("category"))

            post = Post(
                title=data["title"],
                excerpt=data.get("excerpt", ""),
                content=data["content"],
                status=data["status"],
                category=category,
                anime_type=data.get("anime_type", ""),
                rating=data.get("rating"),
                episode_count=data.get("episode_count"),
                release_year=data.get("release_year"),
                studio=data.get("studio", ""),
                author_id=request.user.id,
                author_username=request.user.username,
            )
            post.save()
            messages.success(request, "Post saved")
            return redirect("admin:blogapp_post_manager")
    else:
        form = PostAdminForm()

    context = {
        **admin.site.each_context(request),
        "form": form,
        "posts": Post.objects.order_by("-created_at")[:50],
    }
    return render(request, "admin/blogapp/post_manager.html", context)


def delete_post(request, post_id):
    if not _check_admin(request):
        return redirect("admin:index")

    post = Post.objects(id=post_id).first()
    if not post:
        messages.error(request, "Not found")
        return redirect("admin:blogapp_post_manager")

    post.delete()
    messages.success(request, "Deleted")
    return redirect("admin:blogapp_post_manager")


# =========================
# 🔹 CUSTOM ADMIN URLS
# =========================

# ✅ Save original get_urls FIRST
original_get_urls = admin.site.get_urls


def get_urls():
    urls = original_get_urls()   # ✅ use original, not overridden one

    custom_urls = [
        path("blogapp/", admin.site.admin_view(admin_dashboard), name="blogapp_dashboard"),
        path("blogapp/categories/", admin.site.admin_view(category_manager), name="blogapp_category_manager"),
        path("blogapp/categories/seed/", admin.site.admin_view(seed_default_categories), name="blogapp_seed_categories"),
        path("blogapp/categories/<str:category_id>/delete/", admin.site.admin_view(delete_category), name="blogapp_delete_category"),
        path("blogapp/posts/", admin.site.admin_view(post_manager), name="blogapp_post_manager"),
        path("blogapp/posts/<str:post_id>/delete/", admin.site.admin_view(delete_post), name="blogapp_delete_post"),
    ]

    return custom_urls + urls


# ✅ override AFTER saving original
admin.site.get_urls = get_urls

# =========================
# 🔹 ADMIN UI CUSTOMIZATION
# =========================

admin.site.site_header = "AnimeVerse Admin"
admin.site.site_title = "AnimeVerse Admin"
admin.site.index_title = "Welcome to AnimeVerse Administration"