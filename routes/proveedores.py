from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from models.models import *
from forms.forms import *
from utils.decoradores import login_required

proveedores_bp = Blueprint('proveedores', __name__)

@proveedores_bp.route('/proveedores/', methods=['GET', 'POST'])
@login_required
def registrar_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        existente = Proveedor.query.filter(
            (Proveedor.email == form.email.data) | 
            (Proveedor.telefono == form.telefono.data)
        ).first()

        if existente:
            flash('Ya existe un proveedor con ese correo electrónico o teléfono.', 'error')
        else:
            nuevo = Proveedor(
                nombre=form.nombre.data,
                telefono=form.telefono.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data)
            )
            db.session.add(nuevo)
            db.session.commit()
            flash('Proveedor registrado exitosamente.', 'success')
            return redirect(url_for('proveedores.registrar_proveedor'))

    lista = Proveedor.query.all()
    return render_template('proveedores.html', form=form, proveedores=lista)

# Mostrar proveedores para editar
@proveedores_bp.route('/proveedores/editar/<int:id>', methods=['GET'])
@login_required
def editar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    form = ProveedorForm(obj=proveedor)
    return render_template('proveedores.html', form=form, proveedor=proveedor, modo_edicion=True, proveedor_id=id)

# Actualizar proveedores
@proveedores_bp.route('/proveedores/actualizar/<int:id>', methods=['POST'])
@login_required
def actualizar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    form = ProveedorForm()

    if form.validate_on_submit():
        existente_email = Proveedor.query.filter(Proveedor.email == form.email.data, Proveedor.id != id).first()
        
        if existente_email:
            flash('El correo del proveedor ya está registrado.', 'error')
        else:
            proveedor.nombre = form.nombre.data
            proveedor.telefono = form.telefono.data
            proveedor.email = form.email.data

            if form.password.data:
                proveedor.password = generate_password_hash(form.password.data)

            db.session.commit()
            flash('Proveedor actualizado correctamente.', 'success')
            return redirect(url_for('proveedores.registrar_proveedor'))

    return render_template('proveedores.html', form=form, proveedor=proveedor, modo_edicion=True)

# Eliminar proveedor
@proveedores_bp.route('/proveedores/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    db.session.delete(proveedor)
    db.session.commit()
    flash('Proveedor eliminado correctamente.', 'success')
    return redirect(url_for('proveedores.registrar_proveedor'))
