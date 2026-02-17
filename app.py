from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user,
    login_required, logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import io
from xhtml2pdf import pisa

# ---------------------------------------------------------
# CONFIGURACIÓN PRINCIPAL
# ---------------------------------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-super-secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


# ---------------------------------------------------------
# MODELOS DE BASE DE DATOS
# ---------------------------------------------------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))


class CV(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Datos personales
    nombre = db.Column(db.String(150))
    profesion = db.Column(db.String(150))
    telefono = db.Column(db.String(50))
    direccion = db.Column(db.String(200))
    email_contacto = db.Column(db.String(150))

    # Contenido del CV
    resumen = db.Column(db.Text)
    experiencia = db.Column(db.Text)
    educacion = db.Column(db.Text)
    habilidades = db.Column(db.Text)
    idiomas = db.Column(db.Text)
    certificaciones = db.Column(db.Text)
    proyectos = db.Column(db.Text)

    # Redes sociales
    linkedin = db.Column(db.String(200))
    github = db.Column(db.String(200))
    twitter = db.Column(db.String(200))
    portfolio = db.Column(db.String(200))
    foto_perfil = db.Column(db.String(250))

    # Relación con usuario
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Timestamps
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------------------------------------------------
# RUTAS DE AUTENTICACIÓN
# ---------------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        nuevo_usuario = User(nombre=nombre, email=email, password=password)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        usuario = User.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)
            return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ---------------------------------------------------------
# RUTAS PRINCIPALES
# ---------------------------------------------------------

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


# ---------------------------------------------------------
# CREAR Y GUARDAR CV
# ---------------------------------------------------------

@app.route('/generar', methods=['GET', 'POST'])
@login_required
def generar():
    if request.method == 'GET':
        return render_template('form.html')
    
    datos = request.form
    
    filename = None
    if 'foto_perfil' in request.files:
        file = request.files['foto_perfil']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    nuevo_cv = CV(
        nombre=datos['nombre'],
        profesion=datos['profesion'],
        telefono=datos.get('telefono'),
        direccion=datos.get('direccion'),
        email_contacto=datos.get('email_contacto'),
        resumen=datos.get('resumen'),
        experiencia=datos.get('experiencia'),
        educacion=datos.get('educacion'),
        habilidades=datos.get('habilidades'),
        idiomas=datos.get('idiomas'),
        certificaciones=datos.get('certificaciones'),
        proyectos=datos.get('proyectos'),
        linkedin=datos.get('linkedin'),
        github=datos.get('github'),
        twitter=datos.get('twitter'),
        portfolio=datos.get('portfolio'),
        foto_perfil=filename,
        user_id=current_user.id
    )

    db.session.add(nuevo_cv)
    db.session.commit()

    return render_template('cv_template.html', datos=nuevo_cv)


# ---------------------------------------------------------
# VER LISTA DE CVS DEL USUARIO
# ---------------------------------------------------------

@app.route('/mis-cvs')
@login_required
def mis_cvs():
    cvs = CV.query.filter_by(user_id=current_user.id).all()
    return render_template('mis_cvs.html', cvs=cvs)


# ---------------------------------------------------------
# VER UN CV ESPECÍFICO
# ---------------------------------------------------------

@app.route('/ver-cv/<int:id>')
@login_required
def ver_cv(id):
    cv = CV.query.get_or_404(id)

    if cv.user_id != current_user.id:
        return "No tienes permiso para ver este CV"

    return render_template('cv_template.html', datos=cv)


# ---------------------------------------------------------
# EDITAR CV
# ---------------------------------------------------------

@app.route('/editar-cv/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cv(id):
    cv = CV.query.get_or_404(id)

    if cv.user_id != current_user.id:
        return "No tienes permiso para editar este CV"

    if request.method == 'POST':
        cv.nombre = request.form['nombre']
        cv.profesion = request.form['profesion']
        cv.telefono = request.form.get('telefono')
        cv.direccion = request.form.get('direccion')
        cv.email_contacto = request.form.get('email_contacto')
        cv.resumen = request.form.get('resumen')
        cv.experiencia = request.form.get('experiencia')
        cv.educacion = request.form.get('educacion')
        cv.habilidades = request.form.get('habilidades')
        cv.idiomas = request.form.get('idiomas')
        cv.certificaciones = request.form.get('certificaciones')
        cv.proyectos = request.form.get('proyectos')
        cv.linkedin = request.form.get('linkedin')
        cv.github = request.form.get('github')
        cv.twitter = request.form.get('twitter')
        cv.portfolio = request.form.get('portfolio')

        if 'foto_perfil' in request.files:
            file = request.files['foto_perfil']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cv.foto_perfil = filename

        db.session.commit()
        return redirect(url_for('mis_cvs'))

    return render_template('editar_cv.html', cv=cv)


# ---------------------------------------------------------
# ELIMINAR CV
# ---------------------------------------------------------

@app.route('/eliminar-cv/<int:id>')
@login_required
def eliminar_cv(id):
    cv = CV.query.get_or_404(id)

    if cv.user_id != current_user.id:
        return "No tienes permiso para eliminar este CV"

    db.session.delete(cv)
    db.session.commit()

    return redirect(url_for('mis_cvs'))


# ---------------------------------------------------------
# EXPORTAR PDF
# ---------------------------------------------------------

def link_callback(uri, rel):
    # use short variable names
    sUrl = '/static/'
    sDir = os.path.join(app.root_path, 'static')

    if uri.startswith(sUrl):
        path = os.path.join(sDir, uri.replace(sUrl, "").replace("/", os.sep))
    else:
        return uri

    # make sure that file exists
    if not os.path.isfile(path):
        return uri
        
    return path

@app.route('/exportar-pdf/<int:id>')
@login_required
def exportar_pdf(id):
    cv = CV.query.get_or_404(id)

    if cv.user_id != current_user.id:
        return "No tienes permiso para exportar este CV"

    html = render_template('cv_template.html', datos=cv, is_pdf=True)
    
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(
        io.BytesIO(html.encode("utf-8")), 
        dest=result,
        link_callback=link_callback
    )

    if pisa_status.err:
        return "Error al generar el PDF"

    result.seek(0)
    return send_file(
        result,
        as_attachment=True,
        download_name=f'CV_{secure_filename(cv.nombre)}.pdf',
        mimetype='application/pdf'
    )


# ---------------------------------------------------------
# EJECUCIÓN DEL SERVIDOR
# ---------------------------------------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)