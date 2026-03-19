# AnimeVerse Blog

[🌐 Live Site](https://blog-c7sz.onrender.com)

AnimeVerse is a blog platform built with Django where anime fans can explore reviews, recommendations, and updates from the anime world.  
It’s designed to provide a clean and engaging reading experience while celebrating anime culture.  

---

## ✨ Features

- 📰 **Anime Blog Posts** – Reviews, recommendations, and news articles.  
- 📚 **Pagination** – Easy browsing of posts across pages.  
- 📱 **Responsive Design** – Works on desktop, tablet, and mobile.  
- 🔐 **Admin Dashboard** – Manage blog posts securely through Django’s admin panel.  
- 📂 **Media & Images** – Support for anime-related images and banners with Cloudinary.  
- 🔍 **Search & Filter** – Search posts by title, content, or anime details.  
- 💬 **Comments & Ratings** – Community engagement with post ratings and discussions.  
- 📧 **Newsletter** – Subscribe to anime blog updates.  
- 🚀 **MongoDB Atlas** – NoSQL database for flexible data storage.

---

## 🎯 Purpose

AnimeVerse was created to:  
- Share anime thoughts and recommendations with fans worldwide.  
- Build a hub for anime lovers to explore new and classic titles.  
- Serve as a portfolio project showcasing a full-stack Django blog.  
- Demonstrate modern web development with Django and MongoDB.  

---

## 🛠️ Tech Stack

- **Backend**: Django 5.2.4 (Python)  
- **Database**: MongoDB Atlas (NoSQL)  
- **ODM**: MongoEngine 0.27.0  
- **Frontend**: Django Templates, HTML5, CSS3, Tailwind CSS  
- **Media Storage**: Cloudinary  
- **Hosting**: Render  
- **Static Files**: Whitenoise  

---

## 📋 Prerequisites

Before you begin, make sure you have:
- Python 3.8+ installed
- pip (Python package manager)
- Git installed
- MongoDB Atlas account (free tier available at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas))

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/blog.git
cd Blog
```

### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure MongoDB Atlas

1. **Create a MongoDB Atlas Account**
   - Go to [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
   - Sign up for a free account
   - Create a new project

2. **Create a Cluster**
   - Click "Create a Deployment"
   - Choose "Free" tier (M0)
   - Select your preferred region
   - Click "Create Deployment"

3. **Get Connection String**
   - Go to "Database" → "Clusters"
   - Click "Connect"
   - Choose "Drivers (Python)"
   - Copy the connection string
   - Format: `mongodb+srv://username:password@cluster.mongodb.net/database_name?retryWrites=true&w=majority`

### 5. Setup Environment Variables

Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` and add your MongoDB connection details:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=127.0.0.1,localhost

# MongoDB Configuration
MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?appName=Blog&retryWrites=true&w=majority
MONGODB_DB_NAME=blog_db

# Cloudinary Configuration (Optional)
# CLOUDINARY_CLOUD_NAME=your-cloud-name
# CLOUDINARY_API_KEY=your-api-key
# CLOUDINARY_API_SECRET=your-api-secret
```

### 6. Run the Application

```bash
# Development Server
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

---

## 🔐 Creating Admin User

```bash
python manage.py createsuperuser
```

Then visit: `http://127.0.0.1:8000/admin` to access the admin panel.

---

## 📚 Project Structure

```
Blog/
├── Blog/                 # Project settings
│   ├── settings.py      # Django configuration
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI application
├── blogapp/             # Main app
│   ├── models.py        # MongoEngine models
│   ├── views.py         # View functions
│   ├── urls.py          # App URLs
│   ├── forms.py         # Django forms
│   └── templates/       # HTML templates
├── static/              # Static files (CSS, JS, Images)
├── manage.py            # Django management
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (not tracked)
```

---

## 🌐 Deployment

### Deploy on Render

1. Push your code to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Create a new "Web Service"
4. Connect your GitHub repository
5. Configure environment variables
6. Deploy!

**Environment variables needed on Render:**
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.onrender.com
MONGODB_URI=your-mongodb-atlas-uri
MONGODB_DB_NAME=blog_db
```

---

## 🐛 Troubleshooting

### MongoDB Connection Error
- Check your `MONGODB_URI` in `.env`
- Ensure your IP is whitelisted in MongoDB Atlas
- Verify username and password are URL-encoded

### Import Errors
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Not Found
- MongoDB Atlas will create the database automatically on first connection
- Check the `.env` file configuration  

---

## 📌 Future Roadmap

- 💬 Add comments on posts  
- 🔎 Add search and tag-based filtering  
- 🌙 Add dark mode for better anime vibes  
- 👤 Enable user profiles and custom avatars  

---

## 📸 Screenshots 

![Home Page](static/images/brave_screenshot.png)
