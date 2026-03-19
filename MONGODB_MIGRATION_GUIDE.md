# Django Blog: PostgreSQL to MongoDB Atlas Migration Guide

## Overview
Your Django blog has been successfully migrated from PostgreSQL to **MongoDB Atlas** using **MongoEngine** as the ODM (Object Document Mapper).

## What Changed

### 1. **Dependencies** (requirements.txt)
- ❌ Removed: `psycopg2-binary` (PostgreSQL driver)
- ❌ Removed: `dj-database-url` (PostgreSQL connection string parser)
- ❌ Removed: `sqlparse` (SQL parser)
- ✅ Added: `mongoengine==0.27.0` (MongoDB ODM)
- ✅ Added: `pymongo==4.6.1` (MongoDB Python driver)

### 2. **Database Configuration** (settings.py)
- Replaced PostgreSQL DATABASE_URL parsing with MongoEngine connection
- MongoDB uses a connection URI instead of traditional database settings
- SQLite remains as secondary database for Django's auth, sessions, and admin features

**Old Setup:**
```python
DATABASE_URL = config('DATABASE_URL')
DATABASES = {'default': dj_database_url.parse(DATABASE_URL, ...)}
```

**New Setup:**
```python
MONGODB_URI = config('MONGODB_URI')
MONGODB_DB_NAME = config('MONGODB_DB_NAME')
mongoengine.connect(MONGODB_DB_NAME, host=MONGODB_URI)
```

### 3. **Models** (models.py)
All Django ORM models converted to MongoEngine Documents:

| Django ORM | MongoEngine |
|----------|-----------|
| `models.Model` | `Document` |
| `models.CharField` | `StringField` |
| `models.TextField` | `TextField` |
| `models.ForeignKey` | `ReferenceField` |
| `models.ManyToManyField` | `ListField(ReferenceField(...))` |
| `models.DecimalField` | `FloatField` |
| `models.DateTimeField` | `DateTimeField` |
| `auto_now_add=True` | `default=datetime.utcnow` |

**Key Changes:**
- `Post.author` → Now stores `author_id` (User ID) and `author_username`
- `tags` → Changed to `ListField(ReferenceField(Tag))`
- Image fields store URLs/paths as StringFields (Cloudinary URLs)
- All models use MongoEngine's `.meta` dict for collection configuration

### 4. **Views** (views.py)
Database queries updated to use MongoEngine syntax:

#### Query Syntax Changes

**Filtering:**
```python
# Django ORM
Post.objects.filter(status='published', rating__gte=8.0)

# MongoEngine
Post.objects(status='published', rating__gte=8.0)
```

**Getting Single Objects:**
```python
# Django ORM
post = get_object_or_404(Post, slug=slug, status='published')

# MongoEngine
post = Post.objects(slug=slug, status='published').first()
if not post:
    raise Http404("Post not found")
```

**Ordering:**
```python
# Both use similar syntax
Post.objects(status='published').order_by('-created_at')
```

**Pagination:**
```python
# Paginator requires a list
posts = list(Post.objects(status='published').order_by('-created_at'))
paginator = Paginator(posts, 9)
```

**Many-to-Many Operations:**
```python
# Django ORM
form.save_m2m()  # Saved separately

# MongoEngine
# Tags are saved as part of document during save()
post.save()
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get MongoDB Atlas Connection String
1. Go to https://www.mongodb.com/cloud/atlas (create account if needed)
2. Create a cluster (free tier available)
3. Get your connection string:
   - Clusters → Connect
   - Choose "Python"
   - Copy connection string
   - Format: `mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/blog_db?retryWrites=true&w=majority`

### 3. Configure Environment Variables
Create or update `.env` file:
```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# MongoDB Connection
MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/blog_db?retryWrites=true&w=majority
MONGODB_DB_NAME=blog_db
```

**For Local Development (without MongoDB Atlas):**
```bash
MONGODB_URI=mongodb://localhost:27017/blog_db
MONGODB_DB_NAME=blog_db
```

### 4. Run the Application
```bash
python manage.py runserver
```

## Migrating Existing Data

### If You Have Existing PostgreSQL Data

1. **Export from PostgreSQL:**
   ```bash
   python manage.py dumpdata > data.json
   ```

2. **Create Custom Migration Script** (create `migrate_data.py`):
   ```python
   import json
   import os
   import django
   
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog.settings')
   django.setup()
   
   from blogapp.models import Post, Category, Tag, Comment, Newsletter, Contact
   from django.contrib.auth.models import User
   
   # Read from PostgreSQL dump and create MongoDB documents
   with open('data.json', 'r') as f:
       data = json.load(f)
   
   # Process each model type and create MongoEngine documents
   # (Implementation depends on your data structure)
   ```

3. **Or use Django admin:**
   - Enter Django shell: `python manage.py shell`
   - Define conversion logic for each model
   - Save to MongoDB via MongoEngine

## Important Notes

⚠️ **Django Authorization:**
- Django's `User`, `auth`, `sessions`, and `admin` still use SQLite
- Only blog content (Posts, Comments, Categories, Tags, etc.) use MongoDB
- This hybrid approach is intentional and works well

⚠️ **Admin Interface:**
- Django admin won't work with MongoEngine models directly
- For managing content, create custom admin views or use MongoDB Compass
- Consider using third-party tools like `mongoengine-admin` or `mongonaut`

⚠️ **Authentication:**
- User authentication still uses Django ORM + SQLite
- MongoEngine stores user references by ID + username for compatibility

## Troubleshooting

### "mongoengine.connection.ConnectionFailure: Cannot connect"
- Check `MONGODB_URI` in `.env`
- For MongoDB Atlas, ensure IP is whitelisted in Atlas UI
- Check username and password are URL-encoded

### "DoesNotExist" errors in views
- MongoEngine's `.first()` returns `None` instead of raising exception
- Always check `if not obj: raise Http404()`

### Slugify conflicts
- Current implementation checks uniqueness before saving
- If you need concurrent saves, implement optimistic locking

### Image Fields
- Images must be stored as URLs (Cloudinary) or file paths
- MongoEngine doesn't have native ImageField like Django
- Consider using Cloudinary for production

## Performance Tips

1. **Add Indexes:** Defined in model's `.meta` dict
2. **Pagination:** Always paginate large result sets
3. **Lean Queries:** Use `.only()` and `.exclude()` to fetch specific fields
4. **Bulk Operations:** Use `.update()` and `.delete()` for bulk actions

## Next Steps

1. ✅ Install new dependencies
2. ✅ Set MongoDB Atlas URI in `.env`
3. ✅ Run `python manage.py runserver`
4. ✅ Test create, read, update, delete operations
5. ✅ Configure MongoEngine admin (optional)
6. 🚀 Deploy to production

## References

- [MongoEngine Docs](http://mongoengine.org/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [Django + MongoEngine](http://mongoengine.org/guide/connecting/)
