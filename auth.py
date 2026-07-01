from functools import wraps
from flask import session, redirect, request

# Public Pages
PUBLIC_ROUTES = [
    'home',
    'about',
    'contact',
    'login',
    'register',
    'static',
    'careers',
    'academic_learning'
]

# Login Required
def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'user_id' not in session:
            return redirect('/login')

        return f(*args, **kwargs)

    return decorated_function


# Admin Only
def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'user_id' not in session:
            return redirect('/login')

        role = str(session.get('role', '')).strip().lower()

        if role != 'admin':
            return redirect('/')

        return f(*args, **kwargs)

    return decorated_function


# Member Only
def member_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'user_id' not in session:
            return redirect('/login')

        role = str(session.get('role', '')).strip().lower()

        if role != 'student':
            return redirect('/')

        return f(*args, **kwargs)

    return decorated_function


# Protect Entire Website
def protect_routes(app):

    @app.before_request
    def check_login():

        if request.endpoint is None:
            return

        if request.endpoint in PUBLIC_ROUTES:
            return

        if 'user_id' not in session:
            return redirect('/login')