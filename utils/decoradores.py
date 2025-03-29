from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debes iniciar sesión para acceder a esta página.', 'error')
            return redirect(url_for('login.index'))  # Asegúrate que 'login.index' sea tu ruta de login
        return f(*args, **kwargs)
    return decorated_function
