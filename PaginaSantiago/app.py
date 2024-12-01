from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Clave secreta para sesiones y mensajes flash

# Configurar SQLAlchemy para usar SQLite y crear usuarios.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'  # Ruta del archivo de la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar modificaciones de seguimiento

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Definir el modelo de la base de datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.username}>'

# Crear la base de datos (esto creará el archivo usuarios.db si no existe)heroku login

with app.app_context():
    db.create_all()

# Rutas de la aplicación
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        # Validaciones
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('registro'))

        if Usuario.query.filter_by(username=username).first():
            flash('El usuario ya existe', 'error')
            return redirect(url_for('registro'))

        # Crear un nuevo usuario en la base de datos
        nuevo_usuario = Usuario(username=username, email=email, password=password)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Registro exitoso, ahora puedes iniciar sesión', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')

@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    username = request.form['username']
    password = request.form['password']

    # Verificar las credenciales
    usuario = Usuario.query.filter_by(username=username).first()
    if usuario and usuario.password == password:
        session['username'] = username  # Guardar en la sesión
        flash(f'Bienvenido {username}', 'success')
        return redirect(url_for('ola'))

    flash('Usuario o contraseña incorrectos', 'error')
    return redirect(url_for('login'))

@app.route('/ola')
def ola():
    if 'username' not in session:
        flash('Por favor, inicia sesión', 'error')
        return redirect(url_for('login'))
    return render_template('ola.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
