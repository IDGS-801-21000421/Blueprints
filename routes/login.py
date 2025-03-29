from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from forms.forms import LoginForm
from models.models import Usuarios


login_bp = Blueprint('login', __name__, url_prefix='/')

@login_bp.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        Usuario = Usuarios.query.filter_by(username=form.username.data).first()
        if Usuario and check_password_hash(Usuario.password, form.password.data):
            login_user(Usuario)
            flash('Has iniciado sesión correctamente', 'success')
            return redirect(url_for('usuarios.usuarios')) 
        else:
            flash('Usuarios o contraseña incorrectos', 'danger')
    return render_template('index.html', form=form)

@login_bp.route('/logout')
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('login.index'))
