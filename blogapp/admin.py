from django.contrib import admin

# Note: MongoEngine models (Post, Category, Tag, Comment, Newsletter, Contact) 
# cannot be registered with Django admin directly. 
# For managing MongoDB documents, use:
# 1. MongoDB Compass (GUI)
# 2. mongonaut package
# 3. Custom admin views
# 4. mongoengine-admin package

# Django's built-in User model admin is still available since 
# User authentication uses SQLite database

# Customize admin site
admin.site.site_header = 'AnimeVerse Admin'
admin.site.site_title = 'AnimeVerse Admin'
admin.site.index_title = 'Welcome to AnimeVerse Administration'