import os
import re
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import json
import uuid
import shutil

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave_secreta_super_segura_123')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simulador.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- MODELO DE LA BASE DE DATOS ---
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class HistorialExamen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    nivel = db.Column(db.String(50), nullable=False)
    aciertos = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    porcentaje = db.Column(db.Float, nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('historial', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

class Pregunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nivel = db.Column(db.String(50), nullable=False, default='Superior') 
    materia = db.Column(db.String(50), nullable=False)
    texto_pregunta = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(100), nullable=True) 
    imagen_texto = db.Column(db.Text, nullable=True) 
    opcion_a = db.Column(db.String(200), nullable=False)
    opcion_b = db.Column(db.String(200), nullable=False)
    opcion_c = db.Column(db.String(200), nullable=False)
    opcion_d = db.Column(db.String(200), nullable=False)
    respuesta_correcta = db.Column(db.String(1), nullable=False)
    procedimiento = db.Column(db.Text, nullable=True)

class PreguntaPendiente(db.Model):
    __tablename__ = 'preguntas_pendientes'
    id = db.Column(db.Integer, primary_key=True)
    nivel = db.Column(db.String(50), nullable=False, default='Superior') 
    materia = db.Column(db.String(50), nullable=False)
    texto_pregunta = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(100), nullable=True)
    imagen_texto = db.Column(db.Text, nullable=True) 
    opcion_a = db.Column(db.String(200), nullable=False)
    opcion_b = db.Column(db.String(200), nullable=False)
    opcion_c = db.Column(db.String(200), nullable=False)
    opcion_d = db.Column(db.String(200), nullable=False)
    respuesta_correcta = db.Column(db.String(1), nullable=False)
    procedimiento = db.Column(db.Text, nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)


# ---> CORRECCIÓN ORDEN: Lectura y PreguntaLectura deben ir ANTES que Dudas y Reportes
class Lectura(db.Model):
    __tablename__ = 'lecturas'
    id = db.Column(db.Integer, primary_key=True)
    materia = db.Column(db.String(50), nullable=False, default='Competencia Lectora') # NUEVA COLUMNA
    titulo = db.Column(db.String(250), nullable=False)
    texto_lectura = db.Column(db.Text, nullable=False)
    imagenes = db.Column(db.String(250), nullable=True) 
    referencia = db.Column(db.String(500), nullable=True) 
    preguntas = db.relationship('PreguntaLectura', backref='lectura', lazy=True)

class PreguntaLectura(db.Model):
    __tablename__ = 'preguntas_lectura'
    id = db.Column(db.Integer, primary_key=True)
    id_lectura = db.Column(db.Integer, db.ForeignKey('lecturas.id'), nullable=False)
    nivel = db.Column(db.String(50), default='Superior')
    texto_pregunta = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(250), nullable=True)
    opcion_a = db.Column(db.String(250), nullable=False)
    opcion_b = db.Column(db.String(250), nullable=False)
    opcion_c = db.Column(db.String(250), nullable=False)
    opcion_d = db.Column(db.String(250), nullable=False)
    respuesta_correcta = db.Column(db.String(5), nullable=False)
    procedimiento = db.Column(db.Text, nullable=True) # SE AÑADIÓ PROCEDIMIENTO

class PreguntaDuda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('pregunta.id'), nullable=True) 
    pregunta_lectura_id = db.Column(db.Integer, db.ForeignKey('preguntas_lectura.id'), nullable=True) 
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    usuario = db.relationship('Usuario', backref=db.backref('dudas', lazy=True))
    pregunta = db.relationship('Pregunta', backref=db.backref('marcadas_duda', lazy=True))
    pregunta_lectura = db.relationship('PreguntaLectura', backref=db.backref('marcadas_duda', lazy=True))

class ReportePregunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('pregunta.id'), nullable=True) 
    pregunta_lectura_id = db.Column(db.Integer, db.ForeignKey('preguntas_lectura.id'), nullable=True) 
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    motivo = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    resuelto = db.Column(db.Boolean, default=False)
    
    pregunta = db.relationship('Pregunta', backref=db.backref('reportes', lazy=True))
    pregunta_lectura = db.relationship('PreguntaLectura', backref=db.backref('reportes', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('reportes', lazy=True))

class Sugerencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True) # Opcional si está logueado
    
    usuario = db.relationship('Usuario', backref=db.backref('sugerencias', lazy=True))
# <--- FIN CORRECCIÓN ORDEN



with app.app_context():
    db.create_all()
    import sqlite3
    conn = sqlite3.connect('instance/simulador.db')
    cursor = conn.cursor()
    
    try: cursor.execute("ALTER TABLE usuario ADD COLUMN is_admin BOOLEAN DEFAULT 0")
    except sqlite3.OperationalError: pass

    try: cursor.execute("ALTER TABLE lecturas ADD COLUMN materia VARCHAR(50) DEFAULT 'Competencia Lectora' NOT NULL")
    except sqlite3.OperationalError: pass

    try: cursor.execute("ALTER TABLE pregunta_duda ADD COLUMN pregunta_lectura_id INTEGER REFERENCES preguntas_lectura(id)")
    except sqlite3.OperationalError: pass

    try: cursor.execute("ALTER TABLE reporte_pregunta ADD COLUMN pregunta_lectura_id INTEGER REFERENCES preguntas_lectura(id)")
    except sqlite3.OperationalError: pass

    try: cursor.execute("ALTER TABLE preguntas_lectura ADD COLUMN procedimiento TEXT")
    except sqlite3.OperationalError: pass
    
    # Intentar crear tabla sugerencia si no existe (por si db.create_all ya se corrió antes)
    try: cursor.execute("CREATE TABLE sugerencia (id INTEGER PRIMARY KEY, texto TEXT NOT NULL, fecha DATETIME, usuario_id INTEGER REFERENCES usuario(id))")
    except sqlite3.OperationalError: pass
    
    # ¡SOLO SE GUARDA Y CIERRA UNA VEZ AL FINAL!
    conn.commit()
    conn.close()

    # Crear o actualizar cuenta admin
    admin = Usuario.query.filter_by(username='08amsf').first()
    if not admin:
        admin = Usuario(
            username='08amsf',
            password_hash=generate_password_hash('pel0n100j0tes', method='pbkdf2:sha256'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
    elif not admin.is_admin:
        admin.is_admin = True
        db.session.commit()






from temario import temario_estudio


# --- DECORADOR ADMIN ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(404)  # Ocultar la existencia de las rutas admin
        return f(*args, **kwargs)
    return decorated_function

# --- VERIFICACIÓN DE TÉRMINOS Y CONDICIONES ---
@app.route('/terminos', methods=['GET', 'POST'])
def terminos():
    if request.method == 'POST':
        session['terminos_aceptados'] = True
        return redirect(url_for('seleccion_nivel'))
    return render_template('terminos.html')

@app.before_request
def requerir_terminos():
    rutas_permitidas = ['/terminos', '/login', '/register', '/logout', '/']
    if request.path in rutas_permitidas or request.path.startswith('/static/') or request.path.startswith('/admin/'):
        return None
    if not session.get('terminos_aceptados'):
        flash('Debes aceptar los términos y condiciones antes de utilizar la plataforma.')
        return redirect(url_for('terminos'))

# --- RUTAS DE AUTENTICACIÓN ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if len(username) < 3:
            flash('El nombre de usuario debe tener al menos 3 caracteres.')
            return redirect(url_for('register'))
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.')
            return redirect(url_for('register'))
        
        user_exists = Usuario.query.filter_by(username=username).first()
        if user_exists:
            flash('El nombre de usuario ya está en uso.')
            return redirect(url_for('register'))
            
        new_user = Usuario(username=username, password_hash=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('seleccion_nivel'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = Usuario.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('seleccion_nivel'))
        else:
            flash('Usuario o contraseña incorrectos.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('seleccion_nivel'))

@app.route('/dashboard')
@login_required
def dashboard():
    historial = HistorialExamen.query.filter_by(usuario_id=current_user.id).order_by(HistorialExamen.fecha.asc()).all()
    fechas = [h.fecha.strftime("%Y-%m-%d %H:%M") for h in historial]
    porcentajes = [h.porcentaje for h in historial]
    url_retorno = request.args.get('retorno', '/')
    return render_template('dashboard.html', fechas=json.dumps(fechas), porcentajes=json.dumps(porcentajes), historial=historial[::-1], url_retorno=url_retorno)

@app.route('/flashcards')
@app.route('/flashcards/<nivel>')
def flashcards(nivel="Superior"):
    area = request.args.get('area')
    
    materias_en_db = [m[0] for m in db.session.query(Pregunta.materia).filter_by(nivel=nivel).distinct().all()]
    materias_validas = []
    
    for mat in materias_en_db:
        base_mat = limpiar_materia(mat)
        if obtener_materia_area(base_mat, area) == mat:
            materias_validas.append(mat)
            
    if not materias_validas:
        pregunta = Pregunta.query.filter_by(nivel=nivel).order_by(db.func.random()).first()
    else:
        pregunta = Pregunta.query.filter(
            Pregunta.nivel == nivel,
            Pregunta.materia.in_(materias_validas)
        ).order_by(db.func.random()).first()
        
    materia_limpia = limpiar_materia(pregunta.materia) if pregunta else ""
    
    # CAMBIO: Soportar tanto Competencia Lectora como Inglés en formato bloque
    if materia_limpia in ["Competencia Lectora", "Inglés"]:
        # Filtramos para asegurarnos de que la lectura sea de la materia que el usuario eligió
        lectura = Lectura.query.filter_by(materia=materia_limpia).order_by(db.func.random()).first()
        return render_template('flashcards_lectura.html', lectura=lectura, nivel=nivel, area=area)
        
    return render_template('flashcards.html', pregunta=pregunta, nivel=nivel, area=area, materia_limpia=materia_limpia)
        
    return render_template('flashcards.html', pregunta=pregunta, nivel=nivel, area=area, materia_limpia=materia_limpia)

@app.route('/pregunta/<id>') # Quitamos el <int:id> porque ahora aceptamos L_
def pregunta_individual(id):
    # Buscamos si es una pregunta de lectura (prefijo L_)
    if str(id).startswith('L_'):
        real_id = int(str(id).replace('L_', ''))
        p_lect = db.session.get(PreguntaLectura, real_id)
        if not p_lect:
            flash(f"La pregunta de lectura con ID {real_id} no existe.", "error")
            return redirect(url_for('dudas_menu'))
        # Devolvemos la lectura completa junto a sus preguntas
        lectura = p_lect.lectura
        return render_template('pregunta_lectura_detalle.html', lectura=lectura, nivel=p_lect.nivel)
    
    # Búsqueda normal
    try:
        id_int = int(id)
    except ValueError:
        flash("ID inválido.", "error")
        return redirect(url_for('dudas_menu'))
        
    pregunta = db.session.get(Pregunta, id_int)
    if not pregunta:
        flash(f"Error: La pregunta con ID {id} no existe en la base de datos.", "error")
        return redirect(url_for('dudas_menu'))
    return render_template('pregunta_detalle.html', pregunta=pregunta)

@app.route('/dudas_menu')
def dudas_menu():
    nivel = request.args.get('nivel', 'Superior') # Por defecto Superior si no hay dato
    url_retorno = "/menu_superior" if nivel == "Superior" else "/menu_medio_superior"
    return render_template('dudas_menu.html', url_retorno=url_retorno, nivel=nivel)

@app.route('/buscar_pregunta', methods=['POST'])
def buscar_pregunta():
    id_input = request.form.get('pregunta_id', '').strip()
    if not id_input: 
        flash("Ingresa un ID.", "error")
        return redirect(url_for('dudas_menu'))
    
    # Redirigir a pregunta_individual que ya maneja prefijos
    return redirect(url_for('pregunta_individual', id=id_input))

@app.route('/marcar_duda', methods=['POST'])
def marcar_duda():
    if not current_user.is_authenticated:
        return {"error": "Unauthorized"}, 401
    
    data = request.get_json()
    pregunta_id = data.get('id')
    
    # Verificar si ya existe
    duda_existente = PreguntaDuda.query.filter_by(usuario_id=current_user.id, pregunta_id=pregunta_id).first()
    
    if duda_existente:
        db.session.delete(duda_existente)
        db.session.commit()
        return {"status": "removed"}
    else:
        if str(pregunta_id).startswith('L_'):
            real_id = int(str(pregunta_id).replace('L_', ''))
            nueva_duda = PreguntaDuda(usuario_id=current_user.id, pregunta_lectura_id=real_id)
        else:
            nueva_duda = PreguntaDuda(usuario_id=current_user.id, pregunta_id=int(pregunta_id))
        db.session.add(nueva_duda)
        db.session.commit()
        return {"status": "added"}

@app.route('/mis_dudas')
@login_required
def mis_dudas():
    nivel = request.args.get('nivel', 'Superior')
    dudas = PreguntaDuda.query.filter_by(usuario_id=current_user.id).order_by(PreguntaDuda.fecha.desc()).all()
    return render_template('mis_dudas.html', dudas=dudas, nivel=nivel)

def limpiar_materia(materia):
    if materia and (materia.endswith('_I') or materia.endswith('_M') or materia.endswith('_A')):
        return materia[:-2]
    return materia

def obtener_materia_area(materia, area):
    if materia in ['Física', 'Química', 'Biología'] and area:
        if area == 'Ingeniería y Ciencias Físico Matemáticas':
            return f"{materia}_I"
        elif area == 'Ciencias Médico Biológicas':
            return f"{materia}_M"
        elif area == 'Ciencias Sociales y Administrativas':
            return f"{materia}_A"
    return materia

# --- RUTAS DE LOS MENÚS PRINCIPALES ---
@app.route('/')
def inicio():
    """Entrada principal: siempre muestra términos y condiciones al entrar al sitio."""
    session.pop('terminos_aceptados', None)
    return redirect(url_for('terminos'))

@app.route('/seleccion_nivel')
def seleccion_nivel():
    return render_template('seleccion_nivel.html')

@app.route('/menu_superior')
def menu_superior():
    lista_materias = ["Matemáticas", "Física", "Química", "Biología", "Competencia Escrita", "Competencia Lectora", "Historia y entorno socioeconómico de México", "Inglés"]
    link_apoyo = "https://www.ipn.mx/des/" 
    return render_template('index.html', materias=lista_materias, nivel="Superior", link_material=link_apoyo, url_retorno="/menu_superior")

@app.route('/menu_medio_superior')
def menu_medio_superior():
    # CAMBIO: Diferentes materias para que se note el cambio de menú
    lista_materias = ["Matemáticas Básicas", "Física Básica", "Química Básica", "Biología Básica", "Historia de México", "Formación Cívica y Ética", "Español"]
    link_apoyo = "https://app.dems.ipn.mx/MaterialDeApoyoNMS/"
    return render_template('index.html', materias=lista_materias, nivel="Medio Superior", link_material=link_apoyo, url_retorno="/menu_medio_superior")

# --- RUTAS DE ESTUDIO (AHORA RECIBEN EL NIVEL) ---
@app.route('/estudio/<nivel>')
def menu_estudio(nivel):
    area = request.args.get('area')
    temario_nivel = temario_estudio.get(nivel, {})
    
    temario_filtrado = []
    
    if nivel == 'Superior' and area:
        for mat, temas in temario_nivel.items():
            base_mat = limpiar_materia(mat)
            if obtener_materia_area(base_mat, area) == mat:
                temario_filtrado.append({
                    'original': mat,
                    'limpia': base_mat,
                    'temas': temas
                })
    else:
        for mat, temas in temario_nivel.items():
            temario_filtrado.append({
                'original': mat,
                'limpia': limpiar_materia(mat),
                'temas': temas
            })

    url_retorno = "/menu_superior" if nivel == "Superior" else "/menu_medio_superior"
    return render_template('estudio_menu.html', temario=temario_filtrado, nivel=nivel, area=area, url_retorno=url_retorno)

@app.route('/estudio/<nivel>/<materia>/<tema_id>')
def detalle_estudio(nivel, materia, tema_id):
    temario_nivel = temario_estudio.get(nivel, {})
    if materia in temario_nivel:
        for tema in temario_nivel[materia]:
            if tema['id'] == tema_id:
                url_retorno = f"/estudio/{nivel}"
                return render_template('estudio_detalle.html', materia=materia, tema=tema, nivel=nivel, url_retorno=url_retorno)
    return "Tema no encontrado", 404


def sanitizar_html(texto):
    """Elimina etiquetas <script> y atributos on* peligrosos pero permite LaTeX y HTML seguro."""
    if not texto:
        return texto
    # Eliminar etiquetas <script>...</script>
    texto = re.sub(r'<script[^>]*>.*?</script>', '', texto, flags=re.IGNORECASE | re.DOTALL)
    # Eliminar atributos de eventos (onclick, onerror, onload, etc.)
    texto = re.sub(r'\s+on\w+\s*=\s*["\'][^"\']*["\']', '', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\s+on\w+\s*=\s*\S+', '', texto, flags=re.IGNORECASE)
    return texto

def procesar_archivo_temporal(file_obj):
    if file_obj and file_obj.filename:
        ext = file_obj.filename.split('.')[-1].lower()
        if ext in ['png', 'jpg', 'jpeg', 'webp']:
            nombre_temp = f"pendientes/temp_{uuid.uuid4().hex}.{ext}"
            ruta = os.path.join(app.root_path, 'static', 'img', nombre_temp)
            file_obj.save(ruta)
            return nombre_temp
    return None

@app.route('/agregar_pregunta', methods=['GET', 'POST'])
@app.route('/agregar_pregunta/<nivel>', methods=['GET', 'POST'])
@login_required
def agregar_pregunta(nivel="Superior"):
    if request.method == 'POST':
        imagen_val = procesar_archivo_temporal(request.files.get('imagen_file'))
        
        op_a_val = procesar_archivo_temporal(request.files.get('opcion_a_file')) or sanitizar_html(request.form.get('opcion_a', ''))
        op_b_val = procesar_archivo_temporal(request.files.get('opcion_b_file')) or sanitizar_html(request.form.get('opcion_b', ''))
        op_c_val = procesar_archivo_temporal(request.files.get('opcion_c_file')) or sanitizar_html(request.form.get('opcion_c', ''))
        op_d_val = procesar_archivo_temporal(request.files.get('opcion_d_file')) or sanitizar_html(request.form.get('opcion_d', ''))

        nueva_pregunta = PreguntaPendiente(
            nivel=request.form.get('nivel'), 
            materia=request.form.get('materia'),
            texto_pregunta=sanitizar_html(request.form.get('texto_pregunta')),
            imagen_texto=sanitizar_html(request.form.get('imagen_texto')),
            imagen=imagen_val,
            opcion_a=op_a_val,
            opcion_b=op_b_val,
            opcion_c=op_c_val,
            opcion_d=op_d_val,
            respuesta_correcta=request.form.get('respuesta_correcta'),
            procedimiento=sanitizar_html(request.form.get('procedimiento')),
            usuario_id=current_user.id
        )
        db.session.add(nueva_pregunta)
        db.session.commit()
        flash('¡Gracias por contribuir! Tu pregunta ha sido enviada.', 'success')
        return redirect(url_for('agregar_pregunta', nivel=request.form.get('nivel'))) 
    
    url_retorno = url_for('menu_superior') if nivel == "Superior" else url_for('menu_medio_superior')
    
    return render_template('agregar.html', nivel_actual=nivel, url_retorno=url_retorno)

@app.route('/iniciar_examen', methods=['POST'])
def iniciar_examen():
    modalidad = request.form.get('modalidad')
    nivel = request.form.get('nivel', 'Superior')
    area = request.form.get('area')
    preguntas_seleccionadas = []
    lecturas_seleccionadas = [] # NUEVO: Para guardar los bloques al final
    
    if modalidad == 'general':
        tiempo_minutos = int(request.form.get('tiempo'))
        config_preguntas = {15: 12, 30: 25, 60: 50, 180: 140}
        total_objetivo = config_preguntas.get(tiempo_minutos, 12)
        if nivel == 'Superior':
            if area == 'Ciencias Médico Biológicas':
                pesos = {
                    'Matemáticas': 33/140, 'Competencia Escrita': 20/140,
                    'Competencia Lectora': 20/140, 'Química': 17/140,
                    'Física': 13/140, 'Historia': 10/140,
                    'Inglés': 10/140, 'Biología': 17/140
                }
            else:
                pesos = {
                    'Matemáticas': 37/140, 'Competencia Escrita': 20/140,
                    'Competencia Lectora': 20/140, 'Química': 17/140,
                    'Física': 17/140, 'Historia': 10/140,
                    'Inglés': 10/140, 'Biología': 9/140
                }
        else:
            pesos = {
                'Matemáticas': 37/140, 'Competencia Escrita': 20/140,
                'Competencia Lectora': 20/140, 'Química': 17/140,
                'Física': 17/140, 'Historia': 10/140,
                'Inglés': 10/140, 'Biología': 9/140,
                'Formación Cívica y Ética': 10/140, 'Español': 20/140 # Agregados para NMS
            }

        # CAMBIO: Ahora TODO filtra por "nivel=nivel" y su validación si es por área
        materias_en_db = [m[0] for m in db.session.query(Pregunta.materia).filter_by(nivel=nivel).distinct().all()]
        materias_validas = []
        for mat in materias_en_db:
            base_mat = limpiar_materia(mat)
            if obtener_materia_area(base_mat, area) == mat:
                materias_validas.append(mat)

        for mat in materias_validas:
            p = Pregunta.query.filter_by(materia=mat, nivel=nivel).order_by(db.func.random()).first()
            if p:
                preguntas_seleccionadas.append(p)

        for materia, peso in pesos.items():
            if len(preguntas_seleccionadas) >= total_objetivo: break
            materia_real = obtener_materia_area(materia, area)
            cant_ideal = max(1, int(total_objetivo * peso))
            actuales = len([p for p in preguntas_seleccionadas if p.materia == materia_real])
            if actuales < cant_ideal:
                faltantes_materia = cant_ideal - actuales
                ids_ya_usados = [p.id for p in preguntas_seleccionadas]
                extras = Pregunta.query.filter(
                    Pregunta.materia == materia_real,
                    Pregunta.nivel == nivel, # FILTRO DE NIVEL APLICADO
                    ~Pregunta.id.in_(ids_ya_usados)
                ).order_by(db.func.random()).limit(faltantes_materia).all()
                preguntas_seleccionadas.extend(extras)

        while len(preguntas_seleccionadas) < total_objetivo:
            ids_ya_usados = [p.id for p in preguntas_seleccionadas]
            p_emergencia = Pregunta.query.filter(
                Pregunta.nivel == nivel, # FILTRO DE NIVEL APLICADO
                ~Pregunta.id.in_(ids_ya_usados)
            ).order_by(db.func.random()).first()
            if not p_emergencia: break 
            preguntas_seleccionadas.append(p_emergencia)

        # REGLAS RECTIFICADAS PARA BLOQUES (COMPETENCIA LECTORA E INGLÉS)
        if nivel == 'Superior' or nivel == 'Medio Superior':
            # Limpiamos las individuales para que no se filtren sueltas
            preguntas_seleccionadas = [p for p in preguntas_seleccionadas if p.materia not in ['Competencia Lectora', 'Inglés']]
            nivel_buscar = nivel if nivel == 'Superior' else 'Superior'

            # 1. PREPARAMOS LOS INVENTARIOS DE LECTURAS
            lecturas_esp_todas = Lectura.query.filter_by(materia='Competencia Lectora').join(PreguntaLectura).filter(PreguntaLectura.nivel == nivel_buscar).distinct().all()
            lecturas_ing_todas = Lectura.query.filter_by(materia='Inglés').join(PreguntaLectura).filter(PreguntaLectura.nivel == nivel_buscar).distinct().all()
            
            # Clasificamos las de inglés por su tamaño
            ing_4 = [lec for lec in lecturas_ing_todas if len(lec.preguntas) == 4]
            ing_6 = [lec for lec in lecturas_ing_todas if len(lec.preguntas) == 6]
            ing_8 = [lec for lec in lecturas_ing_todas if len(lec.preguntas) == 8]

            # 2. ASIGNACIÓN SEGÚN EL TIEMPO
            if total_objetivo == 140:
                # 3 HORAS: 2 Español (20p) + 2 Inglés (6p+4p=10p)
                lecturas_seleccionadas.extend(random.sample(lecturas_esp_todas, min(len(lecturas_esp_todas), 2)))
                if ing_6 and ing_4:
                    lecturas_seleccionadas.append(random.choice(ing_6))
                    lecturas_seleccionadas.append(random.choice(ing_4))
                    
            elif total_objetivo == 50:
                # 1 HORA: 1 Español (10p) + Inglés (una de 8p O dos de 4p)
                lecturas_seleccionadas.extend(random.sample(lecturas_esp_todas, min(len(lecturas_esp_todas), 1)))
                opcion_ing = random.choice(['una_de_8', 'dos_de_4'])
                if opcion_ing == 'una_de_8' and ing_8:
                    lecturas_seleccionadas.append(random.choice(ing_8))
                elif len(ing_4) >= 2:
                    lecturas_seleccionadas.extend(random.sample(ing_4, 2))
                    
            elif total_objetivo == 25:
                # 30 MINUTOS: ¡SORPRESA MÁXIMA! 1 Español (10p) Ó 1 Inglés (6p) Ó Ninguna (0p)
                moneda = random.choice(['espanol', 'ingles', 'ninguna'])
                if moneda == 'espanol' and lecturas_esp_todas:
                    lecturas_seleccionadas.append(random.choice(lecturas_esp_todas))
                elif moneda == 'ingles' and ing_6:
                    lecturas_seleccionadas.append(random.choice(ing_6))
                # Si cae 'ninguna', lecturas_seleccionadas se queda vacío y usarás 25 preguntas de materias normales.
                    
            elif total_objetivo == 12:
                # 15 MINUTOS: ¡SORPRESA MÁXIMA! 1 Español (10p) Ó 1 Inglés (4p) Ó Ninguna (0p)
                moneda = random.choice(['espanol', 'ingles', 'ninguna'])
                if moneda == 'espanol' and lecturas_esp_todas:
                    lecturas_seleccionadas.append(random.choice(lecturas_esp_todas))
                elif moneda == 'ingles' and ing_4:
                    lecturas_seleccionadas.append(random.choice(ing_4))
                # Si cae 'ninguna', lecturas_seleccionadas se queda vacío y usarás 12 preguntas de materias normales.

            # 3. RECORTE FINAL DE INDIVIDUALES
            # Ajustamos el total contando exactamente cuántas preguntas tiene cada lectura elegida
            total_preguntas_en_bloques = sum([len(lec.preguntas) for lec in lecturas_seleccionadas])
            limite_individuales = total_objetivo - total_preguntas_en_bloques
            
            # Recortamos de la lista normal de Matemáticas, Física, etc. para que la suma cuadre exacto
            while len(preguntas_seleccionadas) > limite_individuales:
                preguntas_seleccionadas.pop()

    elif modalidad == 'materia':
        materia_elegida = request.form.get('materia')
        # CAMBIO: Agregamos "Inglés" para que también lo trate como Bloque de Lectura
        if materia_elegida in ['Competencia Lectora', 'Inglés']:
            cantidad = int(request.form.get('cantidad'))
            # Calculamos aprox cuántas lecturas sacar según la cantidad pedida
            num_lecturas = max(1, cantidad // 10) 
            
            # IMPORTANTE: Filtrar para que solo traiga lecturas de esa materia específica
            lecturas_disponibles = Lectura.query.filter_by(materia=materia_elegida).all()
            
            lecturas_seleccionadas = random.sample(lecturas_disponibles, min(len(lecturas_disponibles), num_lecturas))
            
            # Calculamos el tiempo exacto basado en las preguntas reales que salieron
            total_preguntas = sum([len(lec.preguntas) for lec in lecturas_seleccionadas])
            tiempo_minutos = int(total_preguntas * 1.5)
        else:
            materia_real = obtener_materia_area(materia_elegida, area)
            cantidad = int(request.form.get('cantidad'))
            tiempo_minutos = int(cantidad * 1.5) 
            preguntas_seleccionadas = Pregunta.query.filter_by(materia=materia_real, nivel=nivel).order_by(db.func.random()).limit(cantidad).all()
    
    random.shuffle(preguntas_seleccionadas)
    return render_template('examen.html', preguntas=preguntas_seleccionadas, lecturas=lecturas_seleccionadas, modalidad=modalidad, tiempo_minutos=tiempo_minutos, nivel=nivel)

# Única versión de /calificar con la lógica para las gráficas
@app.route('/calificar', methods=['POST'])
def calificar():
    datos_formulario = request.form
    lista_ids = request.form.getlist('preguntas_ids')
    total_preguntas = len(lista_ids)
    aciertos = 0
    nivel = request.form.get('nivel', 'Superior')
    areas_mejora = {}
    estadisticas_materias = {}
    
    # NUEVA LISTA: Guardará el resumen individual de cada pregunta
    detalles_examen = []

    for id_str in lista_ids:
        pregunta_id_raw = id_str
        respuesta_usuario = datos_formulario.get(f'resp_{pregunta_id_raw}')
        vio_ayuda = datos_formulario.get(f'ayuda_vista_{pregunta_id_raw}', '0')
        
        if str(pregunta_id_raw).startswith('L_'):
            real_id = int(str(pregunta_id_raw).replace('L_', ''))
            pregunta_db = db.session.get(PreguntaLectura, real_id)
            # CAMBIO: Ahora toma la materia correcta (Inglés o Competencia Lectora)
            materia_limpia = pregunta_db.lectura.materia if pregunta_db else "Desconocida"
        else:
            pregunta_db = db.session.get(Pregunta, int(pregunta_id_raw))
            materia_limpia = limpiar_materia(pregunta_db.materia) if pregunta_db else "Desconocida"
        
        if pregunta_db: 
            if materia_limpia not in estadisticas_materias:
                estadisticas_materias[materia_limpia] = {'total': 0, 'aciertos': 0}
            
            estadisticas_materias[materia_limpia]['total'] += 1
            
            es_correcta = (respuesta_usuario == pregunta_db.respuesta_correcta)
            en_blanco = (respuesta_usuario is None)
            
            if es_correcta and vio_ayuda == '0':
                aciertos += 1
                estadisticas_materias[materia_limpia]['aciertos'] += 1
            else:
                if materia_limpia not in areas_mejora:
                    areas_mejora[materia_limpia] = 0
                areas_mejora[materia_limpia] += 1

            detalles_examen.append({
                'pregunta': pregunta_db,
                'materia_limpia': materia_limpia,
                'respuesta_usuario': respuesta_usuario,
                'es_correcta': es_correcta and vio_ayuda == '0',
                'en_blanco': en_blanco,
                'es_lectura': str(pregunta_id_raw).startswith('L_'),
                'id_original': pregunta_id_raw
            })

    calificacion_escala_10 = (aciertos / total_preguntas) * 10 if total_preguntas > 0 else 0
    porcentaje = (aciertos / total_preguntas) * 100 if total_preguntas > 0 else 0

    nombres_materias = list(estadisticas_materias.keys())
    puntajes_radar = []
    for mat in nombres_materias:
        tot = estadisticas_materias[mat]['total']
        aci = estadisticas_materias[mat]['aciertos']
        porcentaje_mat = (aci / tot) * 100 if tot > 0 else 0
        puntajes_radar.append(round(porcentaje_mat, 1))

    if current_user.is_authenticated:
        nuevo_historial = HistorialExamen(
            usuario_id=current_user.id,
            nivel=nivel,
            aciertos=aciertos,
            total=total_preguntas,
            porcentaje=porcentaje
        )
        db.session.add(nuevo_historial)
        db.session.commit()

    return render_template(
                            'resultados.html', 
                            aciertos=aciertos,
                            total=total_preguntas,
                            porcentaje=porcentaje,
                            calificacion=calificacion_escala_10, 
                            areas_mejora=areas_mejora, 
                            nombres_materias=json.dumps(nombres_materias), 
                            puntajes_radar=json.dumps(puntajes_radar), 
                            detalles_examen=detalles_examen, 
                            nivel=nivel
                            )


@app.route('/guardar_procedimiento', methods=['POST'])
def guardar_procedimiento():
    data = request.json
    pregunta_id_raw = data.get('id')
    nuevo_procedimiento = data.get('procedimiento')

    if str(pregunta_id_raw).startswith('L_'):
        real_id = int(str(pregunta_id_raw).replace('L_', ''))
        pregunta = db.session.get(PreguntaLectura, real_id)
    else:
        pregunta = db.session.get(Pregunta, int(pregunta_id_raw))

    if pregunta:
        pregunta.procedimiento = nuevo_procedimiento
        db.session.commit()
        return {"status": "success"}, 200
    return {"status": "error"}, 400


# --- RUTAS DE REPORTES ---
@app.route('/reportar_pregunta', methods=['POST'])
def reportar_pregunta():
    data = request.get_json()
    pregunta_id_raw = data.get('id')
    motivo = data.get('motivo', '').strip()
    
    if not pregunta_id_raw or not motivo:
        return {"error": "Faltan datos"}, 400
    
    usuario_id = current_user.id if current_user.is_authenticated else None
    
    if str(pregunta_id_raw).startswith('L_'):
        real_id = int(str(pregunta_id_raw).replace('L_', ''))
        nuevo_reporte = ReportePregunta(pregunta_lectura_id=real_id, usuario_id=usuario_id, motivo=motivo)
    else:
        nuevo_reporte = ReportePregunta(pregunta_id=int(pregunta_id_raw), usuario_id=usuario_id, motivo=motivo)

    db.session.add(nuevo_reporte)
    db.session.commit()
    return {"status": "success"}, 200

@app.route('/sugerencia')
def sugerencia_page():
    return render_template('sugerencia.html')

@app.route('/enviar_sugerencia', methods=['POST'])
def enviar_sugerencia():
    texto = request.form.get('texto', '').strip()
    if not texto:
        flash("Por favor, escribe algo antes de enviar.", "error")
        return redirect(url_for('sugerencia_page'))
    
    usuario_id = current_user.id if current_user.is_authenticated else None
    nueva_sugerencia = Sugerencia(texto=texto, usuario_id=usuario_id)
    db.session.add(nueva_sugerencia)
    db.session.commit()
    
    flash("¡Gracias! Tu sugerencia ha sido enviada al buzón.", "success")
    return redirect(url_for('seleccion_nivel'))

@app.route('/admin/sugerencias')
@login_required
@admin_required
def admin_sugerencias():
    sugerencias = Sugerencia.query.order_by(Sugerencia.fecha.desc()).all()
    return render_template('admin_sugerencias.html', sugerencias=sugerencias)

@app.route('/admin/eliminar_sugerencia/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar_sugerencia(id):
    sug = db.session.get(Sugerencia, id)
    if sug:
        db.session.delete(sug)
        db.session.commit()
        return {"status": "success"}, 200
    return {"error": "Sugerencia no encontrada"}, 404


@app.route('/admin/reportes')
@login_required
@admin_required
def admin_reportes():
    reportes = ReportePregunta.query.filter_by(resuelto=False).order_by(ReportePregunta.fecha.desc()).all()
    return render_template('admin_reportes.html', reportes=reportes)

@app.route('/admin/resolver_reporte/<int:id>', methods=['POST'])
@login_required
@admin_required
def resolver_reporte(id):
    reporte = db.session.get(ReportePregunta, id)
    if reporte:
        reporte.resuelto = True
        db.session.commit()
        return {"status": "success"}, 200
    return {"error": "Reporte no encontrado"}, 404

@app.route('/admin/preguntas_pendientes')
@login_required
@admin_required
def admin_preguntas_pendientes():
    pendientes = PreguntaPendiente.query.order_by(PreguntaPendiente.fecha_envio.desc()).all()
    next_pa_n = obtener_siguiente_numero_img()
    max_pregunta_id = db.session.query(db.func.max(Pregunta.id)).scalar()
    next_pregunta_id = (max_pregunta_id or 0) + 1
    return render_template('admin_preguntas_pendientes.html', 
                           pendientes=pendientes, 
                           next_pa_n=next_pa_n, 
                           next_pregunta_id=next_pregunta_id)

def obtener_siguiente_numero_img():
    """Escanea static/img/ buscando archivos p{N}, a{N}, b{N}, c{N}, d{N} y retorna max(N)+1."""
    path = os.path.join(app.root_path, 'static', 'img')
    archivos = os.listdir(path)
    max_n = 0
    pattern = re.compile(r'^[pabcd](\d+)\.(?:png|jpg|jpeg|webp)$', re.IGNORECASE)
    for f in archivos:
        match = pattern.match(f)
        if match:
            n = int(match.group(1))
            if n > max_n:
                max_n = n
    return max_n + 1

def mover_imagen_aprobada(val, prefix_type, next_n):
    """Mueve archivo de pendientes/ a static/img/ con nombre p{N} o a{N}/b{N}/c{N}/d{N}."""
    if not val: return val
    clean_val = val.replace('<p>', '').replace('</p>', '').replace('<br>', '').strip()
    if clean_val.startswith('pendientes/'):
        ext = clean_val.split('.')[-1]
        # prefix_type es '' para pregunta, 'a','b','c','d' para opciones
        prefix = prefix_type if prefix_type else 'p'
        new_name = f"{prefix}{next_n}.{ext}"
        src = os.path.join(app.root_path, 'static', 'img', clean_val)
        dst = os.path.join(app.root_path, 'static', 'img', new_name)
        if os.path.exists(src):
            shutil.move(src, dst)
            return new_name
    return val

def borrar_imagen_disco(val):
    """Borra un archivo de imagen del disco (sea temporal o de producción)."""
    if not val: return
    clean_val = val.replace('<p>', '').replace('</p>', '').replace('<br>', '').strip()
    # Borrar de pendientes
    if clean_val.startswith('pendientes/'):
        src = os.path.join(app.root_path, 'static', 'img', clean_val)
    else:
        # Es una imagen de producción (p5.png, a3.png, etc.)
        src = os.path.join(app.root_path, 'static', 'img', clean_val)
    if os.path.exists(src):
        os.remove(src)

@app.route('/admin/preguntas_pendientes/<int:id>/accion', methods=['POST'])
@login_required
@admin_required
def accion_pregunta_pendiente(id):
    pendiente = db.session.get(PreguntaPendiente, id)
    if not pendiente:
        return {"error": "Pregunta no encontrada"}, 404

    accion = request.form.get('accion')

    if accion == 'aprobar':
        next_n = obtener_siguiente_numero_img()
        
        def gestionar_aprobacion(viejo_val, form_val, prefix):
            # Check if form_val still contains the pendiente path
            clean_form = form_val.replace('<p>', '').replace('</p>', '').replace('<br>', '').strip() if form_val else ''
            
            # If the original was an image but the admin discarded it (e.g. typed text instead)
            if viejo_val and viejo_val.startswith('pendientes/') and clean_form != viejo_val:
                borrar_imagen_disco(viejo_val)
                
            return mover_imagen_aprobada(form_val, prefix, next_n)

        final_img = gestionar_aprobacion(pendiente.imagen, request.form.get('imagen', pendiente.imagen), '')
        final_a = gestionar_aprobacion(pendiente.opcion_a, request.form.get('opcion_a', pendiente.opcion_a), 'a')
        final_b = gestionar_aprobacion(pendiente.opcion_b, request.form.get('opcion_b', pendiente.opcion_b), 'b')
        final_c = gestionar_aprobacion(pendiente.opcion_c, request.form.get('opcion_c', pendiente.opcion_c), 'c')
        final_d = gestionar_aprobacion(pendiente.opcion_d, request.form.get('opcion_d', pendiente.opcion_d), 'd')

        nueva_pregunta = Pregunta(
            nivel=request.form.get('nivel', pendiente.nivel),
            materia=request.form.get('materia', pendiente.materia),
            texto_pregunta=sanitizar_html(request.form.get('texto_pregunta')),
            imagen_texto=sanitizar_html(request.form.get('imagen_texto')),
            imagen=final_img,
            opcion_a=sanitizar_html(final_a),
            opcion_b=sanitizar_html(final_b),
            opcion_c=sanitizar_html(final_c),
            opcion_d=sanitizar_html(final_d),
            respuesta_correcta=request.form.get('respuesta_correcta', pendiente.respuesta_correcta),
            procedimiento=sanitizar_html(request.form.get('procedimiento'))
        )
        db.session.add(nueva_pregunta)
        db.session.delete(pendiente)
        db.session.commit()
        flash('Pregunta aprobada y guardada en el banco oficial.', 'success')
        return redirect(url_for('admin_preguntas_pendientes'))

    elif accion == 'rechazar':
        borrar_imagen_disco(pendiente.imagen)
        borrar_imagen_disco(pendiente.opcion_a)
        borrar_imagen_disco(pendiente.opcion_b)
        borrar_imagen_disco(pendiente.opcion_c)
        borrar_imagen_disco(pendiente.opcion_d)
        
        db.session.delete(pendiente)
        db.session.commit()
        flash('Pregunta rechazada y eliminada.', 'success')
        return redirect(url_for('admin_preguntas_pendientes'))

    return abort(400)

@app.route('/admin')
@login_required
@admin_required
def admin_hub():
    retorno = request.args.get('retorno', '/seleccion_nivel')
    return render_template('admin_hub.html', retorno=retorno)

@app.route('/admin/preguntas_oficiales')
@login_required
@admin_required
def admin_preguntas_oficiales():
    materia_filter = request.args.get('materia')
    orden = request.args.get('orden', 'desc')  # 'asc' o 'desc'
    search_id = request.args.get('search_id', '').strip()
    
    query = Pregunta.query
    
    # Filtro por materia
    if materia_filter:
        query = query.filter_by(materia=materia_filter)
    
    # Búsqueda por ID
    if search_id:
        try:
            query = query.filter(Pregunta.id == int(search_id))
        except ValueError:
            pass
    
    # Orden
    if orden == 'asc':
        query = query.order_by(Pregunta.id.asc())
    else:
        query = query.order_by(Pregunta.id.desc())
    
    if not search_id and not materia_filter:
        preguntas = query.limit(200).all()
    else:
        preguntas = query.all()
    
    materias_db = db.session.query(Pregunta.materia).distinct().all()
    materias = [m[0] for m in materias_db]
    
    return render_template('admin_preguntas_oficiales.html', 
                           preguntas=preguntas, materias=materias, 
                           materia_filtro=materia_filter, orden=orden, search_id=search_id)

@app.route('/admin/eliminar_pregunta/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar_pregunta_oficial(id):
    pregunta = db.session.get(Pregunta, id)
    if pregunta:
        db.session.delete(pregunta)
        db.session.commit()
        return {"status": "success", "message": "Pregunta eliminada"}, 200
    return {"status": "error", "message": "No se encontró la pregunta"}, 404

@app.route('/admin/editar_pregunta/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_editar_pregunta(id):
    pregunta = db.session.get(Pregunta, id)
    if not pregunta:
        flash('Pregunta no encontrada.', 'danger')
        return redirect(url_for('admin_preguntas_oficiales'))

    if request.method == 'GET':
        return render_template('admin_editar_pregunta.html', p=pregunta)

    # --- POST: Procesar la edición ---
    EXTENSIONES = {'png', 'jpg', 'jpeg', 'webp'}
    img_dir = os.path.join(app.root_path, 'static', 'img')

    def es_imagen(nombre):
        if not nombre: return False
        return nombre.lower().rsplit('.', 1)[-1] in EXTENSIONES

    def procesar_campo_imagen(campo_file, campo_text, valor_actual, prefijo):
        """
        Maneja la lógica de imagen para un campo específico.
        - campo_file: nombre del input file en el formulario
        - campo_text: valor de texto del formulario
        - valor_actual: valor actual en la BD
        - prefijo: 'p' para pregunta, 'a','b','c','d' para opciones
        Retorna el nuevo valor para guardar en la BD.
        """
        archivo = request.files.get(campo_file)

        if archivo and archivo.filename:
            # Se subió un archivo nuevo
            ext = archivo.filename.rsplit('.', 1)[-1].lower()
            if ext not in EXTENSIONES:
                return valor_actual  # Extensión no válida, ignorar

            if es_imagen(valor_actual):
                # REEMPLAZAR: borrar la vieja y guardar con el MISMO nombre
                viejo_path = os.path.join(img_dir, valor_actual)
                if os.path.exists(viejo_path):
                    os.remove(viejo_path)
                nuevo_nombre = valor_actual.rsplit('.', 1)[0] + '.' + ext
                archivo.save(os.path.join(img_dir, nuevo_nombre))
                return nuevo_nombre
            else:
                # NUEVA IMAGEN: calcular siguiente N secuencial
                next_n = obtener_siguiente_numero_img()
                nuevo_nombre = f"{prefijo}{next_n}.{ext}"
                archivo.save(os.path.join(img_dir, nuevo_nombre))
                return nuevo_nombre
        else:
            # No se subió archivo, usar el texto del formulario
            nuevo_texto = campo_text
            if nuevo_texto is not None:
                nuevo_texto = nuevo_texto.strip()
                # Si el admin borró el campo y el viejo era imagen, borrar del disco
                if not nuevo_texto and es_imagen(valor_actual):
                    borrar_imagen_disco(valor_actual)
                    return None
                # Si el admin cambió de imagen a texto, borrar la imagen vieja
                if nuevo_texto and es_imagen(valor_actual) and not es_imagen(nuevo_texto):
                    borrar_imagen_disco(valor_actual)
                return nuevo_texto if nuevo_texto else valor_actual
            return valor_actual

    # Procesar cada campo
    pregunta.nivel = request.form.get('nivel', pregunta.nivel)
    pregunta.materia = request.form.get('materia', pregunta.materia)
    pregunta.texto_pregunta = sanitizar_html(request.form.get('texto_pregunta', pregunta.texto_pregunta))
    pregunta.imagen_texto = sanitizar_html(request.form.get('imagen_texto', pregunta.imagen_texto or ''))
    pregunta.respuesta_correcta = request.form.get('respuesta_correcta', pregunta.respuesta_correcta)
    pregunta.procedimiento = sanitizar_html(request.form.get('procedimiento', pregunta.procedimiento or ''))

    # Imagen principal de la pregunta
    pregunta.imagen = procesar_campo_imagen(
        'imagen_file', request.form.get('imagen', pregunta.imagen or ''),
        pregunta.imagen, 'p'
    )

    # Opciones A, B, C, D
    pregunta.opcion_a = sanitizar_html(procesar_campo_imagen(
        'opcion_a_file', request.form.get('opcion_a', pregunta.opcion_a),
        pregunta.opcion_a, 'a'
    ))
    pregunta.opcion_b = sanitizar_html(procesar_campo_imagen(
        'opcion_b_file', request.form.get('opcion_b', pregunta.opcion_b),
        pregunta.opcion_b, 'b'
    ))
    pregunta.opcion_c = sanitizar_html(procesar_campo_imagen(
        'opcion_c_file', request.form.get('opcion_c', pregunta.opcion_c),
        pregunta.opcion_c, 'c'
    ))
    pregunta.opcion_d = sanitizar_html(procesar_campo_imagen(
        'opcion_d_file', request.form.get('opcion_d', pregunta.opcion_d),
        pregunta.opcion_d, 'd'
    ))

    db.session.commit()
    flash(f'Pregunta #{id} actualizada exitosamente.', 'success')
    return redirect(url_for('admin_editar_pregunta', id=id, **request.args))


# --- PÁGINA 404 ---
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)