from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class Usuarios(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(256), nullable=False)

class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)


def insertar_registros_por_defecto(app):
    with app.app_context():
        if not Usuarios.query.filter_by(username='admin').first():
            usuario = Usuarios(
                nombre='Administrador',
                username='admin',
                telefono='5551234567',
                password=generate_password_hash('admin123')
            )
            db.session.add(usuario)
            print('Usuario "admin" insertado.')
        else:
            print('Usuario "admin" ya existe.')

        if not Proveedor.query.filter_by(email='proveedor@demo.com').first():
            proveedor = Proveedor(
                nombre='Proveedor Demo',
                telefono='5559876543',
                email='proveedor@demo.com',
                password=generate_password_hash('demo123')
            )
            db.session.add(proveedor)
            print('Proveedor demo insertado.')
        else:
            print('Proveedor demo ya existe.')

        db.session.commit()