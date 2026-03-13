from flask import Flask, request, render_template_string, redirect, url_for, session, abort, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt
from flask_cors import CORS
from functools import wraps
from datetime import datetime, timedelta
import stripe
import os

app = Flask(__name__)
app.secret_key = "your_super_secret_key_here_please_change"
CORS(app)

# --- Configuration ---
stripe.api_key = "sk_test_XXXXXXXXXXXXXXXXXXXX"

STRIPE_PUBLISHABLE_KEY = "pk_test_YOUR_KEY"

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["EventEase"]
users_col = db["Users"]
events_col = db["Events"]
registrations_col = db["Registrations"]
event_registrations_col = db["EventRegistrations"]
payments_col = db["Payments"]

# --- Helper Functions ---
def is_logged_in():
    return "user_email" in session and "user_expiry" in session and session["user_expiry"] > datetime.now().timestamp()

def current_user():
    if is_logged_in():
        user = users_col.find_one({"email": session["user_email"]})
        if user:
            return user
    session.clear()
    return None

def is_admin():
    user = current_user()
    return user and user.get("role") == "admin"

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    if isinstance(hashed, str):
        hashed = hashed.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login', next=request.url))
        if not is_admin():
            abort(403, description="Admin access required")
        return f(*args, **kwargs)
    return decorated_function

def get_user_registrations(email):
    return list(event_registrations_col.find({"user_email": email}))

# --- Enhanced CSS Styles ---
ENHANCED_CSS = """
<style>
    :root {
        --primary: #4361ee;
        --secondary: #3a0ca3;
        --success: #4cc9f0;
        --danger: #f72585;
        --warning: #f8961e;
        --info: #7209b7;
        --light: #f8f9fa;
        --dark: #212529;
        --gradient: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
        --shadow: 0 10px 30px rgba(0,0,0,0.1);
        --shadow-hover: 0 20px 40px rgba(0,0,0,0.15);
        --radius: 12px;
        --transition: all 0.3s ease;
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: var(--dark);
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }
    
    body::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255,255,255,0.95);
        z-index: -1;
    }
    
    .navbar-glass {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(0,0,0,0.1);
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        padding: 1rem 0;
    }
    
    .navbar-brand {
        font-weight: 800;
        font-size: 1.8rem;
        background: var(--gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .nav-link {
        font-weight: 600;
        padding: 0.5rem 1.2rem !important;
        border-radius: 25px;
        transition: var(--transition);
        margin: 0 5px;
        color: var(--dark) !important;
    }
    
    .nav-link:hover {
        background: var(--gradient);
        color: white !important;
        transform: translateY(-2px);
        box-shadow: var(--shadow);
    }
    
    .nav-link.active {
        background: var(--gradient);
        color: white !important;
    }
    
    .card-glass {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        transition: var(--transition);
        overflow: hidden;
    }
    
    .card-glass:hover {
        transform: translateY(-10px);
        box-shadow: var(--shadow-hover);
    }
    
    .card-img-top {
        height: 200px;
        object-fit: cover;
        transition: transform 0.5s ease;
    }
    
    .card-glass:hover .card-img-top {
        transform: scale(1.05);
    }
    
    .card-title {
        font-weight: 700;
        color: var(--primary);
    }
    
    .badge-gradient {
        background: var(--gradient);
        color: white;
        border: none;
    }
    
    .btn-gradient {
        background: var(--gradient);
        border: none;
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        transition: var(--transition);
    }
    
    .btn-gradient:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(67, 97, 238, 0.3);
        color: white;
    }
    
    .btn-outline-gradient {
        border: 2px solid transparent;
        background: linear-gradient(white, white) padding-box,
                    var(--gradient) border-box;
        color: var(--primary);
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        transition: var(--transition);
    }
    
    .btn-outline-gradient:hover {
        background: var(--gradient);
        color: white;
        transform: translateY(-3px);
    }
    
    .form-glass {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--radius);
        padding: 2.5rem;
        box-shadow: var(--shadow);
    }
    
    .form-control {
        border: 2px solid #e9ecef;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        transition: var(--transition);
    }
    
    .form-control:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
        transform: translateY(-1px);
    }
    
    .table-glass {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: var(--radius);
        overflow: hidden;
        box-shadow: var(--shadow);
    }
    
    .table-glass thead {
        background: var(--gradient);
        color: white;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease;
    }
    
    .hero-section {
        background: var(--gradient);
        border-radius: var(--radius);
        padding: 4rem 2rem;
        margin: 2rem 0;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        opacity: 0.1;
        z-index: 0;
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: var(--radius);
        padding: 2rem;
        text-align: center;
        transition: var(--transition);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: var(--gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .gallery-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .gallery-item {
        border-radius: var(--radius);
        overflow: hidden;
        transition: var(--transition);
    }
    
    .gallery-item:hover {
        transform: scale(1.05);
        box-shadow: var(--shadow-hover);
    }
    
    .gallery-item img {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }
    
    .footer {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(0,0,0,0.1);
        padding: 3rem 0;
        margin-top: 4rem;
    }
    
    @media (max-width: 768px) {
        .hero-section {
            padding: 2rem 1rem;
        }
        .navbar-brand {
            font-size: 1.5rem;
        }
        .gallery-grid {
            grid-template-columns: 1fr;
        }
    }
    
    ::-webkit-scrollbar {
        width: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: var(--gradient);
        border-radius: 10px;
    }
</style>
"""

# --- Navigation Component ---
NAVIGATION = """
<nav class="navbar navbar-expand-lg navbar-glass">
    <div class="container">
        <a class="navbar-brand" href="{{ url_for('home') }}">
            <i class="fas fa-calendar-alt me-2"></i>EventEase
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                {% if user %}
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'dashboard' %}active{% endif %}" 
                           href="{{ url_for('dashboard') }}">
                            <i class="fas fa-tachometer-alt me-1"></i>Dashboard
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'events' %}active{% endif %}" 
                           href="{{ url_for('events') }}">
                            <i class="fas fa-calendar me-1"></i>Events
                        </a>
                    </li>
                    {% if user.role == 'admin' %}
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'admin_panel' %}active{% endif %}" 
                           href="{{ url_for('admin_panel') }}">
                            <i class="fas fa-cog me-1"></i>Admin
                        </a>
                    </li>
                    {% endif %}
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'contact' %}active{% endif %}" 
                           href="{{ url_for('contact') }}">
                            <i class="fas fa-envelope me-1"></i>Contact
                        </a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-user-circle me-1"></i>{{ user.name.split()[0] if user.name else user.email }}
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="{{ url_for('dashboard') }}">
                                <i class="fas fa-user me-2"></i>Profile
                            </a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item text-danger" href="{{ url_for('logout') }}">
                                <i class="fas fa-sign-out-alt me-2"></i>Logout
                            </a></li>
                        </ul>
                    </li>
                {% else %}
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'home' %}active{% endif %}" href="{{ url_for('home') }}">
                            <i class="fas fa-home me-1"></i>Home
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'events' %}active{% endif %}" href="{{ url_for('events') }}">
                            <i class="fas fa-calendar me-1"></i>Events
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'contact' %}active{% endif %}" href="{{ url_for('contact') }}">
                            <i class="fas fa-envelope me-1"></i>Contact
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'login' %}active{% endif %}" href="{{ url_for('login') }}">
                            <i class="fas fa-sign-in-alt me-1"></i>Login
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="btn btn-gradient ms-2" href="{{ url_for('register') }}">
                            <i class="fas fa-user-plus me-1"></i>Sign Up
                        </a>
                    </li>
                {% endif %}
            </ul>
        </div>
    </div>
</nav>
"""

# --- Flash Messages Component ---
FLASH_MESSAGES = """
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        <div class="container mt-3">
            {% for category, message in messages %}
                <div class="alert alert-{{ category }} alert-dismissible fade show shadow" role="alert">
                    <i class="fas 
                        {% if category == 'success' %}fa-check-circle
                        {% elif category == 'danger' %}fa-exclamation-circle
                        {% elif category == 'warning' %}fa-exclamation-triangle
                        {% else %}fa-info-circle
                        {% endif %} me-2"></i>
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        </div>
    {% endif %}
{% endwith %}
"""

# --- Base Template ---
def render_base_template(content, title="EventEase", user=None, **kwargs):
    """Renders content within the base template"""
    base_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        {ENHANCED_CSS}
    </head>
    <body>
        {NAVIGATION}
        {FLASH_MESSAGES}
        
        <main class="container my-4 fade-in">
            {content}
        </main>
        
        <footer class="footer">
            <div class="container">
                <div class="row">
                    <div class="col-md-6">
                        <h4 class="navbar-brand mb-3">EventEase</h4>
                        <p class="text-muted">Modern event management made simple</p>
                        <div class="d-flex gap-3 mt-3">
                            <a href="#" class="text-decoration-none"><i class="fab fa-twitter fa-lg"></i></a>
                            <a href="#" class="text-decoration-none"><i class="fab fa-facebook fa-lg"></i></a>
                            <a href="#" class="text-decoration-none"><i class="fab fa-instagram fa-lg"></i></a>
                            <a href="#" class="text-decoration-none"><i class="fab fa-linkedin fa-lg"></i></a>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <h5>Quick Links</h5>
                        <ul class="list-unstyled">
                            <li><a href="{{ url_for('home') }}" class="text-decoration-none text-muted">Home</a></li>
                            <li><a href="{{ url_for('events') }}" class="text-decoration-none text-muted">Events</a></li>
                            <li><a href="{{ url_for('contact') }}" class="text-decoration-none text-muted">Contact</a></li>
                        </ul>
                    </div>
                    <div class="col-md-3">
                        <h5>Legal</h5>
                        <ul class="list-unstyled">
                            <li><a href="#" class="text-decoration-none text-muted">Privacy Policy</a></li>
                            <li><a href="#" class="text-decoration-none text-muted">Terms of Service</a></li>
                        </ul>
                    </div>
                </div>
                <hr class="my-4">
                <div class="text-center text-muted">
                    <small>© 2024 EventEase. All rights reserved.</small>
                </div>
            </div>
        </footer>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // Auto-dismiss alerts after 5 seconds
            setTimeout(() => {{
                document.querySelectorAll('.alert').forEach(alert => {{
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                }});
            }}, 5000);
            
            // Initialize tooltips
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {{
                return new bootstrap.Tooltip(tooltipTriggerEl);
            }});
        </script>
    </body>
    </html>
    """
    return render_template_string(base_html, user=user, **kwargs)

# --- Routes ---
@app.route("/")
def home():
    """Home page"""
    user = current_user()
    upcoming_events = list(events_col.find({"date": {"$gte": datetime.now()}}).sort("date", 1).limit(3))
    
    content = """
    <div class="hero-section">
        <div class="hero-content text-center">
            <h1 class="display-4 fw-bold mb-4">Welcome to EventEase</h1>
            <p class="lead mb-4">Discover amazing events, register with ease, and create unforgettable memories</p>
            <div class="d-flex justify-content-center gap-3 flex-wrap">
                {% if user %}
                    <a href="{{ url_for('dashboard') }}" class="btn btn-light btn-lg px-4">
                        <i class="fas fa-tachometer-alt me-2"></i>Go to Dashboard
                    </a>
                {% else %}
                    <a href="{{ url_for('register') }}" class="btn btn-light btn-lg px-4">
                        <i class="fas fa-user-plus me-2"></i>Get Started
                    </a>
                    <a href="{{ url_for('login') }}" class="btn btn-outline-light btn-lg px-4">
                        <i class="fas fa-sign-in-alt me-2"></i>Login
                    </a>
                {% endif %}
                <a href="{{ url_for('events') }}" class="btn btn-outline-light btn-lg px-4">
                    <i class="fas fa-calendar me-2"></i>Browse Events
                </a>
            </div>
        </div>
    </div>
    
    <div class="row mt-5 g-4">
        <div class="col-md-4">
            <div class="card-glass text-center h-100">
                <div class="card-body p-4">
                    <div class="bg-primary bg-opacity-10 rounded-circle d-inline-flex p-3 mb-3">
                        <i class="fas fa-calendar-check fa-2x text-primary"></i>
                    </div>
                    <h4 class="card-title mb-3">Easy Registration</h4>
                    <p class="text-muted">Register for events in minutes with our streamlined process</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card-glass text-center h-100">
                <div class="card-body p-4">
                    <div class="bg-success bg-opacity-10 rounded-circle d-inline-flex p-3 mb-3">
                        <i class="fas fa-shield-alt fa-2x text-success"></i>
                    </div>
                    <h4 class="card-title mb-3">Secure Payments</h4>
                    <p class="text-muted">Safe payment processing with Stripe integration</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card-glass text-center h-100">
                <div class="card-body p-4">
                    <div class="bg-warning bg-opacity-10 rounded-circle d-inline-flex p-3 mb-3">
                        <i class="fas fa-images fa-2x text-warning"></i>
                    </div>
                    <h4 class="card-title mb-3">Event Galleries</h4>
                    <p class="text-muted">Browse photos from past events</p>
                </div>
            </div>
        </div>
    </div>
    
    {% if upcoming_events %}
    <div class="mt-5">
        <h2 class="mb-4">Upcoming Events</h2>
        <div class="row g-4">
            {% for event in upcoming_events %}
            <div class="col-md-4">
                <div class="card-glass h-100">
                    {% if event.image_url %}
                    <img src="{{ event.image_url }}" class="card-img-top" alt="{{ event.title }}">
                    {% else %}
                    <div class="card-img-top bg-primary bg-opacity-10 d-flex align-items-center justify-content-center">
                        <i class="fas fa-calendar-alt fa-3x text-primary"></i>
                    </div>
                    {% endif %}
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <h5 class="card-title mb-0">{{ event.title }}</h5>
                            <span class="badge badge-gradient">
                                {% if event.price and event.price > 0 %}
                                ${{ (event.price / 100) | round(2) }}
                                {% else %}
                                Free
                                {% endif %}
                            </span>
                        </div>
                        <p class="text-muted small">{{ event.date.strftime('%b %d, %Y') }}</p>
                        <p class="card-text">{{ event.description[:100] }}{% if event.description|length > 100 %}...{% endif %}</p>
                        <a href="{{ url_for('view_event_details', event_id=event._id|string) }}" 
                           class="btn btn-outline-gradient w-100">
                            View Details
                        </a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        {% if upcoming_events|length > 3 %}
        <div class="text-center mt-4">
            <a href="{{ url_for('events') }}" class="btn btn-gradient">View All Events</a>
        </div>
        {% endif %}
    </div>
    {% endif %}
    """
    
    return render_template_string(content, user=user, upcoming_events=upcoming_events)
    return render_base_template(content, title="Home | EventEase", user=user, upcoming_events=upcoming_events)

@app.route("/events")
def events():
    """Public events page"""
    user = current_user()
    upcoming = list(events_col.find({"date": {"$gte": datetime.now()}}).sort("date", 1))
    past = list(events_col.find({"date": {"$lt": datetime.now()}}).sort("date", -1))
    
    content = """
    <h1 class="mb-4">Browse Events</h1>
    
    <h2 class="mt-5 mb-4">Upcoming Events ({{ upcoming|length }})</h2>
    {% if upcoming %}
    <div class="row g-4">
        {% for event in upcoming %}
        <div class="col-md-6 col-lg-4">
            <div class="card-glass h-100">
                {% if event.image_url %}
                <img src="{{ event.image_url }}" class="card-img-top" alt="{{ event.title }}">
                {% endif %}
                <div class="card-body">
                    <h5 class="card-title">{{ event.title }}</h5>
                    <p class="text-muted"><i class="far fa-calendar me-2"></i>{{ event.date.strftime('%b %d, %Y') }}</p>
                    <p class="card-text">{{ event.description[:150] }}{% if event.description|length > 150 %}...{% endif %}</p>
                    <div class="d-flex justify-content-between align-items-center mt-3">
                        <span class="badge badge-gradient">
                            {% if event.price and event.price > 0 %}
                            ${{ (event.price / 100) | round(2) }}
                            {% else %}
                            Free
                            {% endif %}
                        </span>
                        <a href="{{ url_for('view_event_details', event_id=event._id|string) }}" 
                           class="btn btn-outline-gradient btn-sm">
                            Details <i class="fas fa-arrow-right ms-1"></i>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <div class="text-center py-5">
        <i class="fas fa-calendar-times fa-3x text-muted mb-3"></i>
        <h4 class="text-muted">No upcoming events</h4>
    </div>
    {% endif %}
    
    {% if past %}
    <h2 class="mt-5 mb-4">Past Events</h2>
    <div class="gallery-grid">
        {% for event in past %}
        {% if event.image_url %}
        <div class="gallery-item">
            <img src="{{ event.image_url }}" alt="{{ event.title }}" 
                 data-bs-toggle="tooltip" title="{{ event.title }}">
        </div>
        {% endif %}
        {% endfor %}
    </div>
    {% endif %}
    """
    
    return render_base_template(content, title="Events | EventEase", user=user, 
                              upcoming=upcoming, past=past)

@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration"""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "user")
        
        if not all([name, email, password]):
            flash("All fields are required", "danger")
            return redirect(url_for("register"))
        
        if users_col.find_one({"email": email}):
            flash("Email already registered", "warning")
            return redirect(url_for("login"))
        
        hashed = hash_password(password)
        users_col.insert_one({
            "name": name,
            "email": email,
            "password": hashed,
            "role": role,
            "created_at": datetime.now()
        })
        
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))
    
    content = """
    <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
            <div class="form-glass">
                <h2 class="text-center mb-4">Create Account</h2>
                <form method="POST">
                    <div class="mb-3">
                        <label class="form-label">Full Name</label>
                        <input type="text" name="name" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Email Address</label>
                        <input type="email" name="email" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" name="password" class="form-control" required>
                    </div>
                    <div class="mb-4">
                        <label class="form-label">Account Type</label>
                        <select name="role" class="form-control" required>
                            <option value="user">Regular User</option>
                            <option value="admin">Administrator</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-gradient w-100">Create Account</button>
                    <p class="text-center mt-3">
                        Already have an account? <a href="{{ url_for('login') }}" class="text-decoration-none">Login here</a>
                    </p>
                </form>
            </div>
        </div>
    </div>
    """
    return render_base_template(content, title="Register | EventEase")

@app.route("/login", methods=["GET", "POST"])
def login():
    """User login"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = users_col.find_one({"email": email})
        
        if user and check_password(password, user["password"]):
            session["user_email"] = user["email"]
            session["user_expiry"] = (datetime.now() + timedelta(hours=24)).timestamp()
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(request.args.get("next") or url_for("dashboard"))
        
        flash("Invalid email or password", "danger")
    
    content = """
    <div class="row justify-content-center">
        <div class="col-md-8 col-lg-5">
            <div class="form-glass">
                <h2 class="text-center mb-4">Welcome Back</h2>
                <form method="POST">
                    <div class="mb-3">
                        <label class="form-label">Email Address</label>
                        <input type="email" name="email" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" name="password" class="form-control" required>
                    </div>
                    <div class="mb-3 form-check">
                        <input type="checkbox" class="form-check-input" id="remember">
                        <label class="form-check-label" for="remember">Remember me</label>
                    </div>
                    <button type="submit" class="btn btn-gradient w-100">Login</button>
                    <p class="text-center mt-3">
                        Don't have an account? <a href="{{ url_for('register') }}" class="text-decoration-none">Sign up here</a>
                    </p>
                </form>
            </div>
        </div>
    </div>
    """
    return render_base_template(content, title="Login | EventEase")

@app.route("/logout")
def logout():
    """User logout"""
    session.clear()
    flash("You have been logged out successfully", "info")
    return redirect(url_for("home"))

@app.route("/dashboard")
@login_required
def dashboard():
    """User dashboard"""
    user = current_user()
    
    # Get user's event registrations
    user_regs = get_user_registrations(user["email"])
    registered_event_ids = [str(reg["event_id"]) for reg in user_regs]
    
    # Get upcoming events
    upcoming_events = list(events_col.find({"date": {"$gte": datetime.now()}}).sort("date", 1))
    
    # Get registered events with details
    registered_events = []
    for reg in user_regs:
        event = events_col.find_one({"_id": reg["event_id"]})
        if event:
            event["reg_status"] = "Paid" if reg.get("paid") else "Registered"
            registered_events.append(event)
    
    content = """
    <div class="row mb-4">
        <div class="col-md-8">
            <h1 class="mb-3">Dashboard</h1>
            <p class="lead">Welcome back, <strong>{{ user.name }}</strong>!</p>
        </div>
        <div class="col-md-4 text-md-end">
            <a href="{{ url_for('events') }}" class="btn btn-gradient">
                <i class="fas fa-plus me-2"></i>Find Events
            </a>
        </div>
    </div>
    
    <div class="row g-4 mb-5">
        <div class="col-md-3">
            <div class="stat-card">
                <div class="stat-number">{{ upcoming_events|length }}</div>
                <div class="text-muted">Upcoming Events</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card">
                <div class="stat-number">{{ registered_events|length }}</div>
                <div class="text-muted">Your Registrations</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card">
                <div class="stat-number">{{ paid_count }}</div>
                <div class="text-muted">Paid Events</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card">
                <div class="stat-number">{{ user.role|title }}</div>
                <div class="text-muted">Account Type</div>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col-lg-8">
            <div class="card-glass mb-4">
                <div class="card-body">
                    <h3 class="card-title mb-4">Upcoming Events</h3>
                    {% if upcoming_events %}
                    <div class="row g-3">
                        {% for event in upcoming_events[:4] %}
                        <div class="col-md-6">
                            <div class="border rounded p-3">
                                <div class="d-flex justify-content-between mb-2">
                                    <h6 class="mb-0">{{ event.title }}</h6>
                                    <span class="badge {% if event._id|string in registered_event_ids %}bg-success{% else %}bg-primary{% endif %}">
                                        {% if event._id|string in registered_event_ids %}Registered{% else %}Available{% endif %}
                                    </span>
                                </div>
                                <p class="text-muted small mb-2">{{ event.date.strftime('%b %d, %Y') }}</p>
                                <a href="{{ url_for('view_event_details', event_id=event._id|string) }}" 
                                   class="btn btn-sm btn-outline-gradient w-100">
                                    View Details
                                </a>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                    {% else %}
                    <p class="text-muted text-center py-4">No upcoming events</p>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <div class="col-lg-4">
            <div class="card-glass">
                <div class="card-body">
                    <h3 class="card-title mb-4">Your Events</h3>
                    {% if registered_events %}
                    <div class="list-group list-group-flush">
                        {% for event in registered_events %}
                        <div class="list-group-item border-0 px-0">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <h6 class="mb-0">{{ event.title }}</h6>
                                    <small class="text-muted">{{ event.date.strftime('%b %d') }}</small>
                                </div>
                                <span class="badge {% if event.price and event.price > 0 %}bg-primary{% else %}bg-success{% endif %}">
                                    {{ event.reg_status }}
                                </span>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                    {% else %}
                    <p class="text-muted text-center py-4">No registered events</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    """
    
    paid_count = len([e for e in registered_events if e.get('price', 0) > 0])
    
    return render_base_template(content, title="Dashboard | EventEase", user=user,
                              upcoming_events=upcoming_events, 
                              registered_events=registered_events,
                              registered_event_ids=registered_event_ids,
                              paid_count=paid_count)

@app.route("/event/<event_id>")
@login_required
def view_event_details(event_id):
    """Event details page"""
    user = current_user()
    event = events_col.find_one({"_id": ObjectId(event_id)})
    
    if not event:
        flash("Event not found", "danger")
        return redirect(url_for("dashboard"))
    
    # Check if user is registered
    is_registered = bool(event_registrations_col.find_one({
        "user_email": user["email"],
        "event_id": ObjectId(event_id)
    }))
    
    content = """
    <div class="row">
        <div class="col-lg-8">
            <div class="card-glass">
                {% if event.image_url %}
                <img src="{{ event.image_url }}" class="card-img-top" alt="{{ event.title }}">
                {% endif %}
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-4">
                        <div>
                            <h1 class="mb-2">{{ event.title }}</h1>
                            <p class="text-muted mb-0">
                                <i class="far fa-calendar me-2"></i>
                                {{ event.date.strftime('%A, %B %d, %Y') }}
                            </p>
                        </div>
                        <span class="badge badge-gradient fs-5">
                            {% if event.price and event.price > 0 %}
                            ${{ (event.price / 100) | round(2) }}
                            {% else %}
                            Free
                            {% endif %}
                        </span>
                    </div>
                    
                    <div class="mb-4">
                        <h5>Description</h5>
                        <p class="lead">{{ event.description }}</p>
                    </div>
                    
                    {% if event.gallery_images and event.gallery_images|length > 0 %}
                    <div class="mb-4">
                        <h5>Gallery Preview</h5>
                        <div class="gallery-grid">
                            {% for img in event.gallery_images[:4] %}
                            <div class="gallery-item">
                                <img src="{{ img }}" alt="Event image">
                            </div>
                            {% endfor %}
                        </div>
                        {% if event.gallery_images|length > 4 %}
                        <div class="text-center mt-3">
                            <a href="#" class="btn btn-outline-gradient">
                                View All {{ event.gallery_images|length }} Photos
                            </a>
                        </div>
                        {% endif %}
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <div class="col-lg-4">
            <div class="card-glass sticky-top" style="top: 20px;">
                <div class="card-body">
                    <h4 class="mb-4">Registration</h4>
                    
                    {% if is_registered %}
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle me-2"></i>
                        You are registered for this event
                    </div>
                    {% endif %}
                    
                    <div class="d-grid gap-2">
                        {% if not is_registered %}
                            {% if event.price and event.price > 0 %}
                            <a href="{{ url_for('initiate_payment', event_id=event._id|string) }}" 
                               class="btn btn-gradient btn-lg">
                                <i class="fas fa-credit-card me-2"></i>
                                Register Now - ${{ (event.price / 100) | round(2) }}
                            </a>
                            {% else %}
                            <a href="{{ url_for('register_event', event_id=event._id|string) }}" 
                               class="btn btn-success btn-lg">
                                <i class="fas fa-user-plus me-2"></i>
                                Register for Free
                            </a>
                            {% endif %}
                        {% endif %}
                        
                        {% if event.gallery_images and event.gallery_images|length > 0 %}
                        <a href="#" class="btn btn-outline-gradient">
                            <i class="fas fa-images me-2"></i>
                            View Gallery
                        </a>
                        {% endif %}
                        
                        <a href="{{ url_for('events') }}" class="btn btn-outline-secondary">
                            <i class="fas fa-arrow-left me-2"></i>
                            Back to Events
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return render_base_template(content, title=f"{event['title']} | EventEase", user=user,
                              event=event, is_registered=is_registered)

@app.route("/register_event/<event_id>")
@login_required
def register_event(event_id):
    """Register for free event"""
    user = current_user()
    event = events_col.find_one({"_id": ObjectId(event_id)})
    
    if not event:
        flash("Event not found", "danger")
        return redirect(url_for("dashboard"))
    
    # Check if already registered
    existing = event_registrations_col.find_one({
        "user_email": user["email"],
        "event_id": ObjectId(event_id)
    })
    
    if existing:
        flash("Already registered for this event", "info")
        return redirect(url_for("view_event_details", event_id=event_id))
    
    # Register for free event
    event_registrations_col.insert_one({
        "user_email": user["email"],
        "event_id": ObjectId(event_id),
        "event_title": event["title"],
        "registration_date": datetime.now(),
        "paid": False
    })
    
    flash(f"Successfully registered for {event['title']}!", "success")
    return redirect(url_for("view_event_details", event_id=event_id))

@app.route("/initiate_payment/<event_id>")
@login_required
def initiate_payment(event_id):
    """Initiate payment for paid event"""
    user = current_user()
    event = events_col.find_one({"_id": ObjectId(event_id)})
    
    if not event:
        flash("Event not found", "danger")
        return redirect(url_for("dashboard"))
    
    if not event.get("price") or event["price"] <= 0:
        return redirect(url_for("register_event", event_id=event_id))
    
    content = """
    <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
            <div class="card-glass">
                <div class="card-body text-center">
                    <h2 class="mb-4">Complete Registration</h2>
                    <div class="mb-4">
                        <h4>{{ event.title }}</h4>
                        <p class="text-muted">{{ event.date.strftime('%b %d, %Y') }}</p>
                        <h3 class="text-primary">${{ (event.price / 100) | round(2) }}</h3>
                    </div>
                    
                    <form action="{{ url_for('process_payment', event_id=event_id) }}" method="POST">
                        <script src="https://checkout.stripe.com/checkout.js" 
                                class="stripe-button"
                                data-key="{{ STRIPE_PUBLISHABLE_KEY }}"
                                data-amount="{{ event.price }}"
                                data-name="EventEase"
                                data-description="{{ event.title }}"
                                data-image="https://stripe.com/img/documentation/checkout/marketplace.png"
                                data-locale="auto"
                                data-currency="usd">
                        </script>
                    </form>
                    
                    <div class="mt-4">
                        <a href="{{ url_for('view_event_details', event_id=event_id) }}" 
                           class="btn btn-outline-secondary">
                            Cancel
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return render_base_template(content, title="Payment | EventEase", user=user, 
                              event=event, STRIPE_PUBLISHABLE_KEY=STRIPE_PUBLISHABLE_KEY)

@app.route("/process_payment/<event_id>", methods=["POST"])
@login_required
def process_payment(event_id):
    """Process Stripe payment"""
    user = current_user()
    event = events_col.find_one({"_id": ObjectId(event_id)})
    
    if not event:
        flash("Event not found", "danger")
        return redirect(url_for("dashboard"))
    
    try:
        # Create Stripe charge
        charge = stripe.Charge.create(
            amount=event["price"],
            currency="usd",
            source=request.form["stripeToken"],
            description=f"Event: {event['title']} - {user['email']}",
        )
        
        if charge.status == "succeeded":
            # Record payment
            payments_col.insert_one({
                "user_email": user["email"],
                "event_id": ObjectId(event_id),
                "amount": event["price"],
                "stripe_charge_id": charge.id,
                "status": "succeeded",
                "created_at": datetime.now()
            })
            
            # Register user for event
            event_registrations_col.insert_one({
                "user_email": user["email"],
                "event_id": ObjectId(event_id),
                "event_title": event["title"],
                "registration_date": datetime.now(),
                "paid": True
            })
            
            content = """
            <div class="text-center py-5">
                <div class="mb-4">
                    <i class="fas fa-check-circle fa-5x text-success"></i>
                </div>
                <h2 class="mb-3">Payment Successful!</h2>
                <p class="lead mb-4">You are now registered for <strong>{{ event.title }}</strong></p>
                <div class="card-glass d-inline-block p-4">
                    <p><strong>Amount:</strong> ${{ (event.price / 100) | round(2) }}</p>
                    <p><strong>Transaction ID:</strong> {{ charge.id[:20] }}...</p>
                    <p><strong>Date:</strong> {{ datetime.now().strftime('%b %d, %Y %I:%M %p') }}</p>
                </div>
                <div class="mt-4">
                    <a href="{{ url_for('dashboard') }}" class="btn btn-gradient me-2">
                        Go to Dashboard
                    </a>
                    <a href="{{ url_for('view_event_details', event_id=event_id) }}" class="btn btn-outline-gradient">
                        View Event
                    </a>
                </div>
            </div>
            """
            
            return render_base_template(content, title="Payment Successful | EventEase", user=user,
                                      event=event, charge=charge)
    
    except stripe.error.StripeError as e:
        flash(f"Payment failed: {str(e)}", "danger")
        return redirect(url_for("initiate_payment", event_id=event_id))

@app.route("/admin")
@admin_required
def admin_panel():
    """Admin panel"""
    user = current_user()
    
    # Get stats
    total_users = users_col.count_documents({})
    total_events = events_col.count_documents({})
    total_registrations = event_registrations_col.count_documents({})
    
    # Get recent data
    recent_events = list(events_col.find().sort("date", -1).limit(5))
    recent_users = list(users_col.find().sort("created_at", -1).limit(5))
    recent_payments = list(payments_col.find().sort("created_at", -1).limit(5))
    
    content = """
    <div class="row mb-4">
        <div class="col-md-8">
            <h1 class="mb-3">Admin Panel</h1>
            <p class="lead">Welcome, Administrator</p>
        </div>
        <div class="col-md-4 text-md-end">
            <a href="{{ url_for('create_event') }}" class="btn btn-gradient">
                <i class="fas fa-plus me-2"></i>Create Event
            </a>
        </div>
    </div>
    
    <div class="row g-4 mb-5">
        <div class="col-md-3">
            <div class="stat-card">
                <div class="stat-number">{{ total_users }}</div>
                <div class="text-muted">Total Users</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card">
                <div class="stat-number">{{ total_events }}</div>
                <div class="text-muted">Total Events</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card">
                <div class="stat-number">{{ total_registrations }}</div>
                <div class="text-muted">Registrations</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card">
                <div class="stat-number">{{ recent_payments|length }}</div>
                <div class="text-muted">Recent Payments</div>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col-lg-8">
            <div class="card-glass mb-4">
                <div class="card-body">
                    <h4 class="card-title mb-4">Recent Events</h4>
                    {% if recent_events %}
                    <div class="table-responsive">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Event</th>
                                    <th>Date</th>
                                    <th>Price</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for event in recent_events %}
                                <tr>
                                    <td>{{ event.title }}</td>
                                    <td>{{ event.date.strftime('%Y-%m-%d') }}</td>
                                    <td>
                                        {% if event.price and event.price > 0 %}
                                        ${{ (event.price / 100) | round(2) }}
                                        {% else %}
                                        Free
                                        {% endif %}
                                    </td>
                                    <td>
                                        <a href="{{ url_for('edit_event', event_id=event._id|string) }}" 
                                           class="btn btn-sm btn-outline-primary">
                                            Edit
                                        </a>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    {% else %}
                    <p class="text-muted text-center py-4">No events found</p>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <div class="col-lg-4">
            <div class="card-glass mb-4">
                <div class="card-body">
                    <h4 class="card-title mb-4">Recent Payments</h4>
                    {% if recent_payments %}
                    <div class="list-group list-group-flush">
                        {% for payment in recent_payments %}
                        <div class="list-group-item border-0 px-0">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="mb-0">${{ (payment.amount / 100) | round(2) }}</h6>
                                    <small class="text-muted">{{ payment.user_email[:20] }}...</small>
                                </div>
                                <span class="badge bg-success">Paid</span>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                    {% else %}
                    <p class="text-muted text-center py-4">No payments found</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    """
    
    return render_base_template(content, title="Admin Panel | EventEase", user=user,
                              total_users=total_users, total_events=total_events,
                              total_registrations=total_registrations,
                              recent_events=recent_events, recent_users=recent_users,
                              recent_payments=recent_payments)

@app.route("/admin/create_event", methods=["GET", "POST"])
@admin_required
def create_event():
    """Create new event"""
    if request.method == "POST":
        title = request.form.get("title")
        date_str = request.form.get("date")
        description = request.form.get("description")
        price_str = request.form.get("price", "0")
        image_url = request.form.get("image_url")
        gallery_images = request.form.get("gallery_images", "")
        
        try:
            event_date = datetime.strptime(date_str, "%Y-%m-%d")
            price = int(float(price_str) * 100)
            gallery_list = [url.strip() for url in gallery_images.split(",") if url.strip()]
            
            events_col.insert_one({
                "title": title,
                "date": event_date,
                "description": description,
                "price": price,
                "image_url": image_url,
                "gallery_images": gallery_list,
                "created_at": datetime.now()
            })
            
            flash("Event created successfully!", "success")
            return redirect(url_for("admin_panel"))
        
        except Exception as e:
            flash(f"Error creating event: {str(e)}", "danger")
    
    content = """
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="card-glass">
                <div class="card-body">
                    <h2 class="mb-4">Create New Event</h2>
                    <form method="POST">
                        <div class="row g-3">
                            <div class="col-md-12">
                                <label class="form-label">Event Title</label>
                                <input type="text" name="title" class="form-control" required>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">Date</label>
                                <input type="date" name="date" class="form-control" required>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">Price ($)</label>
                                <input type="number" step="0.01" name="price" class="form-control" value="0">
                            </div>
                            <div class="col-md-12">
                                <label class="form-label">Main Image URL</label>
                                <input type="url" name="image_url" class="form-control" 
                                       placeholder="https://example.com/image.jpg">
                            </div>
                            <div class="col-md-12">
                                <label class="form-label">Gallery Image URLs (comma separated)</label>
                                <textarea name="gallery_images" class="form-control" rows="3"
                                          placeholder="https://example.com/img1.jpg, https://example.com/img2.jpg"></textarea>
                            </div>
                            <div class="col-md-12">
                                <label class="form-label">Description</label>
                                <textarea name="description" class="form-control" rows="5" required></textarea>
                            </div>
                            <div class="col-md-12">
                                <div class="d-flex gap-2">
                                    <button type="submit" class="btn btn-gradient">Create Event</button>
                                    <a href="{{ url_for('admin_panel') }}" class="btn btn-outline-secondary">Cancel</a>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    """
    return render_base_template(content, title="Create Event | EventEase", user=current_user())

@app.route("/admin/edit_event/<event_id>", methods=["GET", "POST"])
@admin_required
def edit_event(event_id):
    """Edit existing event"""
    event = events_col.find_one({"_id": ObjectId(event_id)})
    
    if not event:
        flash("Event not found", "danger")
        return redirect(url_for("admin_panel"))
    
    if request.method == "POST":
        title = request.form.get("title")
        date_str = request.form.get("date")
        description = request.form.get("description")
        price_str = request.form.get("price", "0")
        image_url = request.form.get("image_url")
        gallery_images = request.form.get("gallery_images", "")
        
        try:
            event_date = datetime.strptime(date_str, "%Y-%m-%d")
            price = int(float(price_str) * 100)
            gallery_list = [url.strip() for url in gallery_images.split(",") if url.strip()]
            
            events_col.update_one(
                {"_id": ObjectId(event_id)},
                {"$set": {
                    "title": title,
                    "date": event_date,
                    "description": description,
                    "price": price,
                    "image_url": image_url,
                    "gallery_images": gallery_list,
                    "updated_at": datetime.now()
                }}
            )
            
            flash("Event updated successfully!", "success")
            return redirect(url_for("admin_panel"))
        
        except Exception as e:
            flash(f"Error updating event: {str(e)}", "danger")
    
    # Format data for form
    event_price = event.get("price", 0)
    price_display = event_price / 100 if event_price else 0
    gallery_images_list = event.get("gallery_images", [])
    gallery_str = ", ".join(gallery_images_list)
    event_date = event.get("date")
    date_str = event_date.strftime("%Y-%m-%d") if isinstance(event_date, datetime) else str(event_date)
    
    content = f"""
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="card-glass">
                <div class="card-body">
                    <h2 class="mb-4">Edit Event</h2>
                    <form method="POST">
                        <div class="row g-3">
                            <div class="col-md-12">
                                <label class="form-label">Event Title</label>
                                <input type="text" name="title" class="form-control" 
                                       value="{event.get('title', '')}" required>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">Date</label>
                                <input type="date" name="date" class="form-control" 
                                       value="{date_str}" required>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">Price ($)</label>
                                <input type="number" step="0.01" name="price" class="form-control" 
                                       value="{price_display}">
                            </div>
                            <div class="col-md-12">
                                <label class="form-label">Main Image URL</label>
                                <input type="url" name="image_url" class="form-control" 
                                       value="{event.get('image_url', '')}">
                            </div>
                            <div class="col-md-12">
                                <label class="form-label">Gallery Image URLs (comma separated)</label>
                                <textarea name="gallery_images" class="form-control" rows="3">{gallery_str}</textarea>
                            </div>
                            <div class="col-md-12">
                                <label class="form-label">Description</label>
                                <textarea name="description" class="form-control" rows="5" required>{event.get('description', '')}</textarea>
                            </div>
                            <div class="col-md-12">
                                <div class="d-flex gap-2">
                                    <button type="submit" class="btn btn-gradient">Update Event</button>
                                    <a href="{{ url_for('admin_panel') }}" class="btn btn-outline-secondary">Cancel</a>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    """
    return render_base_template(content, title="Edit Event | EventEase", user=current_user(), event=event)

@app.route("/admin/delete_event/<event_id>")
@admin_required
def delete_event(event_id):
    """Delete event"""
    result = events_col.delete_one({"_id": ObjectId(event_id)})
    
    if result.deleted_count > 0:
        # Also delete related registrations and payments
        event_registrations_col.delete_many({"event_id": ObjectId(event_id)})
        payments_col.delete_many({"event_id": ObjectId(event_id)})
        
        flash("Event deleted successfully", "success")
    else:
        flash("Event not found", "danger")
    
    return redirect(url_for("admin_panel"))

@app.route("/contact")
def contact():
    """Contact page"""
    content = """
    <div class="row justify-content-center">
        <div class="col-lg-10">
            <div class="card-glass">
                <div class="card-body">
                    <div class="row">
                        <div class="col-lg-6">
                            <h2 class="mb-4">Get in Touch</h2>
                            <p class="lead mb-4">Have questions? We'd love to hear from you.</p>
                            
                            <div class="mb-4">
                                <h5><i class="fas fa-envelope text-primary me-2"></i>Email</h5>
                                <p>support@eventease.com</p>
                            </div>
                            
                            <div class="mb-4">
                                <h5><i class="fas fa-phone text-success me-2"></i>Phone</h5>
                                <p>+1 (555) 123-4567</p>
                            </div>
                            
                            <div class="mb-4">
                                <h5><i class="fas fa-map-marker-alt text-warning me-2"></i>Address</h5>
                                <p>123 Event Street<br>City, State 12345</p>
                            </div>
                        </div>
                        
                        <div class="col-lg-6">
                            <form action="#" method="POST">
                                <div class="mb-3">
                                    <label class="form-label">Name</label>
                                    <input type="text" class="form-control" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Email</label>
                                    <input type="email" class="form-control" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Subject</label>
                                    <input type="text" class="form-control" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Message</label>
                                    <textarea class="form-control" rows="5" required></textarea>
                                </div>
                                <button type="submit" class="btn btn-gradient w-100">Send Message</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return render_base_template(content, title="Contact | EventEase", user=current_user())

if __name__ == "__main__":
    app.run(debug=True, port=5000)