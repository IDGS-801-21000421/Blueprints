from flask import Blueprint, request, jsonify, redirect, render_template
from flask_login import login_user, logout_user, login_required
from models.models import *
from utils.decoradores import login_required
ventas_bp = Blueprint('ventas', __name__)

# Ruta para ventas
@ventas_bp.route('/ventas', methods=['POST', 'GET'])  
@login_required
def ventas():
    return render_template('punto-venta.html') 
