from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from models.models import *
from forms.forms import *
from utils.decoradores import login_required

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios', methods=['GET', 'POST'])
@login_required
def usuarios():
    form = UsuarioForm()
    if form.validate_on_submit():
        existente_usuario = Usuarios.query.filter_by(username=form.username.data).first()
        existente_telefono = Usuarios.query.filter_by(telefono=form.telefono.data).first()

        if existente_usuario:
            flash('El nombre de usuario ya está en uso.', 'error')
        elif existente_telefono:
            flash('El número de teléfono ya está registrado.', 'error')
        elif not form.password.data:
            flash('La contraseña es obligatoria para registrar un usuario.', 'error')
        else:
            nuevo = Usuarios(
                nombre=form.nombre.data,
                username=form.username.data,
                telefono=form.telefono.data,
                password=generate_password_hash(form.password.data),
            )
            db.session.add(nuevo)
            db.session.commit()
            flash('Usuario registrado exitosamente.', 'success')
            return redirect(url_for('usuarios.usuarios'))


    lista = Usuarios.query.all()
    return render_template('usuarios.html', form=form, usuarios=lista, modo_edicion=False)


@usuarios_bp.route('/usuarios/editar/<int:id>', methods=['GET'])
@login_required
def editar_usuario(id):
    usuario = Usuarios.query.get_or_404(id)
    form = UsuarioForm(obj=usuario)
    lista = Usuarios.query.all()
    return render_template('usuarios.html', form=form, usuarios=lista, modo_edicion=True, usuario_id=id)

@usuarios_bp.route('/usuarios/actualizar/<int:id>', methods=['POST'])
@login_required
def actualizar_usuario(id):
    usuario = Usuarios.query.get_or_404(id)
    form = UsuarioForm()

    if form.validate_on_submit():
        existente_usuario = Usuarios.query.filter(Usuarios.username == form.username.data, Usuarios.id != id).first()
        existente_telefono = Usuarios.query.filter(Usuarios.telefono == form.telefono.data, Usuarios.id != id).first()

        if existente_usuario:
            flash('El nombre de usuario ya está en uso.', 'error')
        elif existente_telefono:
            flash('El número de teléfono ya está registrado.', 'error')
        else:
            usuario.nombre = form.nombre.data
            usuario.username = form.username.data
            usuario.telefono = form.telefono.data

            if form.password.data:
                usuario.password = generate_password_hash(form.password.data)

            db.session.commit()
            flash('Usuario actualizado correctamente.', 'success')
            return redirect(url_for('usuarios.usuarios'))

    lista = Usuarios.query.all()
    return render_template('usuarios.html', form=form, usuarios=lista, modo_edicion=True, usuario_id=id)


@usuarios_bp.route('/usuarios/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_usuario(id):
    usuario = Usuarios.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('usuarios.usuarios'))
