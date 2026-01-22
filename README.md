1. DJANGO PROJECT STRUCTURE
Here's what we created:
django/                          ← Main project folder
├── venv/                        ← Virtual environment (isolated Python)
├── manage.py                    ← Command-line tool for Django
├── mysite/                      ← Project configuration folder
│   ├── __init__.py
│   ├── settings.py              ← Main settings (apps, database, etc.)
│   ├── urls.py                  ← Main URL router
│   ├── wsgi.py                  ← Web server gateway
│   └── asgi.py                  ← Async server gateway
├── pages/                       ← App 1 (Home page)
│   ├── templates/
│   │   └── home.html
│   ├── views.py
│   └── urls.py
├── app1/                        ← App 2 (Triangular Sum)
│   ├── templates/
│   │   └── app1/
│   │       └── triangular_sum.html
│   ├── views.py
│   └── urls.py
└── app2/                        ← App 3 (Bloch Sphere)
    ├── templates/
    │   └── bloch.html
    ├── views.py
    └── urls.py

2. KEY CONCEPTS
Project vs App

Project (mysite/) = The entire website
App (pages/, app1/, app2/) = Individual features/modules

Think of it like:

Project = A shopping mall
Apps = Individual stores (clothing store, food court, electronics)

Each app is self-contained and reusable.

3. THE REQUEST-RESPONSE FLOW
Here's what happens when you visit http://127.0.0.1:8000/app1/triangular-sum/:
1. Browser sends request
   ↓
2. Django receives it at manage.py runserver
   ↓
3. Goes to mysite/urls.py (main router)
   ↓
4. Matches pattern: path('app1/', include('app1.urls'))
   ↓
5. Goes to app1/urls.py
   ↓
6. Matches pattern: path('triangular-sum/', views.triangular_sum)
   ↓
7. Calls the view function in app1/views.py
   ↓
8. View processes request and renders template
   ↓
9. Returns HTML response to browser
   ↓
10. Browser displays the page

4. URL ROUTING (The Phone Directory)
Main Router (mysite/urls.py):
pythonurlpatterns = [
    path('admin/', admin.site.urls),           # Django admin panel
    path('', include('pages.urls')),           # Homepage (empty path)
    path('app1/', include('app1.urls')),       # Triangular sum app
    path('app2/', include('app2.urls')),       # Bloch sphere app
]
How it works:

path('', ...) → Matches http://127.0.0.1:8000/
path('app1/', ...) → Matches http://127.0.0.1:8000/app1/...
include() → Delegates to the app's own urls.py


App Router (app1/urls.py):
pythonapp_name = 'app1'  # Namespace for URL names

urlpatterns = [
    path('triangular-sum/', views.triangular_sum, name='triangular_sum'),
]
Full URL becomes:

Main: app1/
App: triangular-sum/
Result: http://127.0.0.1:8000/app1/triangular-sum/

The name parameter:

Allows you to reference URLs by name instead of hardcoding
In templates: {% url 'app1:triangular_sum' %}
Much better than hardcoding /app1/triangular-sum/


5. VIEWS (The Brain)
Views are Python functions that handle requests and return responses.
Simple View (pages/views.py):
pythonfrom django.shortcuts import render

def home(request):
    return render(request, 'home.html')
What happens:

Takes a request object (contains info about the HTTP request)
render() combines a template with data
Returns an HTML response

View with Context (passing data to template):
pythondef home(request):
    context = {
        'title': 'My Django App',
        'apps': ['Triangular Sum', 'Bloch Sphere']
    }
    return render(request, 'home.html', context)
In the template, you can use:
html<h1>{{ title }}</h1>
{% for app in apps %}
    <p>{{ app }}</p>
{% endfor %}

6. TEMPLATES (The Face)
Templates are HTML files with Django template language.
Template Location:
Django looks for templates in:

app_name/templates/ folder
app_name/templates/app_name/ folder (better practice)

Why the extra folder?

Avoids name conflicts between apps
app1/templates/app1/triangular_sum.html is clearer than app1/templates/triangular_sum.html

Template Tags:
html<!-- Variables -->
{{ variable_name }}

<!-- URL linking -->
<a href="{% url 'app1:triangular_sum' %}">Link</a>

<!-- Conditionals -->
{% if user.is_authenticated %}
    <p>Welcome!</p>
{% endif %}

<!-- Loops -->
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}

<!-- Load static files -->
{% load static %}
<img src="{% static 'images/logo.png' %}">

7. SETTINGS.PY (The Control Center)
INSTALLED_APPS:
pythonINSTALLED_APPS = [
    'django.contrib.admin',      # Built-in: Admin panel
    'django.contrib.auth',       # Built-in: User authentication
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # Built-in: Static files (CSS, JS, images)
    'pages',                      # Your apps
    'app1',
    'app2',
]
```

**You must register every app here** or Django won't recognize it!

---

## 8. HOW OUR APPS WORK TOGETHER

### **Homepage Flow:**
```
User visits: http://127.0.0.1:8000/
    ↓
mysite/urls.py: path('', include('pages.urls'))
    ↓
pages/urls.py: path('', views.home, name='home')
    ↓
pages/views.py: def home(request)
    ↓
Renders: pages/templates/home.html
    ↓
User sees: Homepage with links to app1 and app2
```

### **Clicking on Triangular Sum:**
```
User clicks: {% url 'app1:triangular_sum' %}
    ↓
Resolves to: /app1/triangular-sum/
    ↓
mysite/urls.py: path('app1/', include('app1.urls'))
    ↓
app1/urls.py: path('triangular-sum/', views.triangular_sum)
    ↓
app1/views.py: def triangular_sum(request)
    ↓
Renders: app1/templates/app1/triangular_sum.html
```

---

## 9. NAMESPACE PATTERN

Notice we used:
- `app_name = 'app1'` in `app1/urls.py`
- `{% url 'app1:triangular_sum' %}` in templates

**Why?**
- Multiple apps might have a view called "home"
- Namespaces prevent conflicts: `app1:home` vs `app2:home`

---

## 10. DJANGO MVT PATTERN

Django follows **MVT** (Model-View-Template):
```
┌─────────┐
│  Model  │  ← Database (we didn't use this yet)
└────┬────┘
     │
┌────▼────┐
│  View   │  ← Business logic (views.py)
└────┬────┘
     │
┌────▼────────┐
│  Template   │  ← Presentation (HTML files)
└─────────────┘
What we built:

Views: views.py files (business logic)
Templates: HTML files (what users see)
Models: Not used yet (would handle database)


11. COMMON DJANGO COMMANDS
bash# Create new app
python manage.py startapp app_name

# Run development server
python manage.py runserver

# Check for errors
python manage.py check

# Create database tables (when using models)
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

---

## 12. FILE RESPONSIBILITIES SUMMARY

| File | Purpose | Example |
|------|---------|---------|
| `settings.py` | Project configuration | Register apps, set database |
| `mysite/urls.py` | Main URL router | Route to different apps |
| `app/urls.py` | App-specific URLs | Define app's URL patterns |
| `views.py` | Business logic | Handle requests, return responses |
| `templates/` | HTML files | What users see |
| `models.py` | Database structure | Define data (not used yet) |

---

## 13. YOUR PROJECT FLOW DIAGRAM
```
┌──────────────────────────────────────────────────────┐
│                   User's Browser                      │
│              http://127.0.0.1:8000/                   │
└───────────────────────┬──────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────┐
│              mysite/urls.py (Router)                  │
│  ┌───────────────────────────────────────────────┐  │
│  │ path('', include('pages.urls'))               │  │
│  │ path('app1/', include('app1.urls'))           │  │
│  │ path('app2/', include('app2.urls'))           │  │
│  └───────────────────────────────────────────────┘  │
└────────┬─────────────────┬─────────────────┬─────────┘
         │                 │                 │
    ┌────▼────┐       ┌────▼────┐      ┌────▼────┐
    │ pages/  │       │  app1/  │      │  app2/  │
    │ urls.py │       │ urls.py │      │ urls.py │
    └────┬────┘       └────┬────┘      └────┬────┘
         │                 │                 │
    ┌────▼────┐       ┌────▼────┐      ┌────▼────┐
    │ pages/  │       │  app1/  │      │  app2/  │
    │views.py │       │views.py │      │views.py │
    └────┬────┘       └────┬────┘      └────┬────┘
         │                 │                 │
    ┌────▼────────┐  ┌────▼─────────────┐ ┌▼──────┐
    │  home.html  │  │triangular_sum.html│ │bloch  │
    │             │  │                   │ │.html  │
    └─────────────┘  └───────────────────┘ └───────┘

14. KEY TAKEAWAYS

Apps are modular - Each app is independent and reusable
URL routing is hierarchical - Main URLs → App URLs → Views
Views connect everything - They're the glue between URLs and templates
Templates use special syntax - {{ }} for variables, {% %} for logic
Always register apps - in INSTALLED_APPS
Use URL names - Never hardcode URLs, use {% url 'app:name' %}