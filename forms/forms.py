from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, AnyOf, Email, Optional


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class UsuarioForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2)])
    username = StringField('Usuarios', validators=[DataRequired(), Length(min=3)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(min=10, max=15)])
    password = PasswordField('Contraseña', validators=[Optional()])
    submit = SubmitField('Registrar')
    
class ProveedorForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Correo', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[Optional()])
    submit = SubmitField('Registrar Proveedor')