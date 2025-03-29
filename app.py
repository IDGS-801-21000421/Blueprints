from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from models.models import * 
from config import DevelopmentConfig

# Importación de Blueprints
from routes.login import login_bp
from routes.usuarios import usuarios_bp
from routes.proveedores import proveedores_bp
from routes.p_venta import ventas_bp

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    csrf.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'login.index'
    login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuarios.query.get(int(user_id))
    
    app.register_blueprint(login_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(proveedores_bp)
    app.register_blueprint(ventas_bp)

    with app.app_context():
        db.create_all()
        insertar_registros_por_defecto(app)        

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', debug=True)
