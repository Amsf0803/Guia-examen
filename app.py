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
    opcion_a = db.Column(db.String(200), nullable=False)
    opcion_b = db.Column(db.String(200), nullable=False)
    opcion_c = db.Column(db.String(200), nullable=False)
    opcion_d = db.Column(db.String(200), nullable=False)
    respuesta_correcta = db.Column(db.String(1), nullable=False)
    procedimiento = db.Column(db.Text, nullable=True)

# ---> CORRECCIÓN ORDEN: Lectura y PreguntaLectura deben ir ANTES que Dudas y Reportes
class Lectura(db.Model):
    __tablename__ = 'lecturas'
    id = db.Column(db.Integer, primary_key=True)
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
# <--- FIN CORRECCIÓN ORDEN

with app.app_context():
    db.create_all()
    # Migración: agregar columna is_admin si no existe
    import sqlite3
    conn = sqlite3.connect('instance/simulador.db')
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE usuario ADD COLUMN is_admin BOOLEAN DEFAULT 0")
    except sqlite3.OperationalError: pass

    # MIGRACIÓN: Nuevas columnas para Competencia Lectora
    try:
        cursor.execute("ALTER TABLE pregunta_duda ADD COLUMN pregunta_lectura_id INTEGER REFERENCES preguntas_lectura(id)")
    except sqlite3.OperationalError: pass
    try:
        cursor.execute("ALTER TABLE reporte_pregunta ADD COLUMN pregunta_lectura_id INTEGER REFERENCES preguntas_lectura(id)")
    except sqlite3.OperationalError: pass
    # Añadiendo campo de procedimiento que faltaba en PreguntaLectura
    try:
        cursor.execute("ALTER TABLE preguntas_lectura ADD COLUMN procedimiento TEXT")
    except sqlite3.OperationalError: pass
    
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
    
    # NUEVO: Si la materia es Competencia Lectora, devolvemos la lectura completa
    if materia_limpia == "Competencia Lectora":
        # En la tabla Pregunta no hay Comp. Lectora (según las nuevas reglas)
        # Así que si llegamos aquí es porque se pidió específicamente o se coló.
        # Buscamos una lectura aleatoria.
        lectura = Lectura.query.order_by(db.func.random()).first()
        return render_template('flashcards_lectura.html', lectura=lectura, nivel=nivel, area=area)
        
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
    lista_materias = ["Matemáticas", "Física", "Química", "Competencia Escrita", "Competencia Lectora", "Historia y entorno socioeconómico de México", "Inglés"]
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

@app.route('/agregar_pregunta', methods=['GET', 'POST'])
@app.route('/agregar_pregunta/<nivel>', methods=['GET', 'POST'])
@login_required
def agregar_pregunta(nivel="Superior"):
    if request.method == 'POST':
        nueva_pregunta = Pregunta(
            nivel=request.form.get('nivel'), 
            materia=request.form.get('materia'),
            texto_pregunta=sanitizar_html(request.form.get('texto_pregunta')),
            opcion_a=sanitizar_html(request.form.get('opcion_a')),
            opcion_b=sanitizar_html(request.form.get('opcion_b')),
            opcion_c=sanitizar_html(request.form.get('opcion_c')),
            opcion_d=sanitizar_html(request.form.get('opcion_d')),
            respuesta_correcta=request.form.get('respuesta_correcta'),
            procedimiento=sanitizar_html(request.form.get('procedimiento'))
        )
        db.session.add(nueva_pregunta)
        db.session.commit()
        flash('¡Pregunta guardada exitosamente!', 'success')
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

        # REGLAS RECTIFICADAS PARA COMPETENCIA LECTORA (AL FINAL)
        if nivel == 'Superior' or nivel == 'Medio Superior':
            num_lecturas = 0
            if total_objetivo == 140: num_lecturas = 2
            elif total_objetivo == 50: num_lecturas = 1
            
            if num_lecturas > 0:
                # SOLUCIÓN: Hacemos un JOIN con PreguntaLectura para poder filtrar por su nivel
                nivel_buscar = nivel if nivel == 'Superior' else 'Superior'
                lecturas_disponibles = Lectura.query.join(PreguntaLectura).filter(PreguntaLectura.nivel == nivel_buscar).distinct().all()

                lecturas_seleccionadas = random.sample(lecturas_disponibles, min(len(lecturas_disponibles), num_lecturas))

    elif modalidad == 'materia':
        materia_elegida = request.form.get('materia')
        if materia_elegida == 'Competencia Lectora':
            cantidad = int(request.form.get('cantidad'))
            num_lecturas = max(1, cantidad // 10)
            lecturas_disponibles = Lectura.query.all()
            lecturas_seleccionadas = random.sample(lecturas_disponibles, min(len(lecturas_disponibles), num_lecturas))
            tiempo_minutos = int(num_lecturas * 10 * 1.5)
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
            materia_limpia = "Competencia Lectora"
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

# --- PÁGINA 404 ---
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)