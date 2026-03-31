from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import json

app = Flask(__name__)
# Aquí le decimos a Flask que cree un archivo llamado 'simulador.db' en la misma carpeta
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simulador.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODELO DE LA BASE DE DATOS ---
class Pregunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    materia = db.Column(db.String(50), nullable=False)
    texto_pregunta = db.Column(db.Text, nullable=False)
    
    # NUEVA COLUMNA: Guardará el nombre de la imagen (puede estar vacía)
    imagen = db.Column(db.String(100), nullable=True) 
    
    opcion_a = db.Column(db.String(200), nullable=False)
    opcion_b = db.Column(db.String(200), nullable=False)
    opcion_c = db.Column(db.String(200), nullable=False)
    opcion_d = db.Column(db.String(200), nullable=False)
    
    respuesta_correcta = db.Column(db.String(1), nullable=False)
    procedimiento = db.Column(db.Text, nullable=True)

# Creamos la base de datos y las tablas al ejecutar la app
with app.app_context():
    db.create_all()

# --- RUTAS ---
@app.route('/')
def index():
    lista_materias = [
        "Matemáticas", "Física", "Química", 
        "Competencia Escrita", "Competencia Lectora", 
        "Historia", "Inglés"
    ]
    return render_template('index.html', materias=lista_materias)

@app.route('/agregar_pregunta', methods=['GET', 'POST'])
def agregar_pregunta():
    if request.method == 'POST':
        nueva_pregunta = Pregunta(
            materia=request.form['materia'],
            texto_pregunta=request.form['texto_pregunta'],
            opcion_a=request.form['opcion_a'],
            opcion_b=request.form['opcion_b'],
            opcion_c=request.form['opcion_c'],
            opcion_d=request.form['opcion_d'],
            respuesta_correcta=request.form['respuesta_correcta'],
            procedimiento=request.form['procedimiento']
        )
        
        db.session.add(nueva_pregunta)
        db.session.commit()
        
        return redirect(url_for('agregar_pregunta')) 
        
    # Corrección aquí: debe apuntar a la plantilla correcta
    return render_template('agregar.html')

@app.route('/iniciar_examen', methods=['POST'])
def iniciar_examen():
    modalidad = request.form.get('modalidad')
    preguntas_seleccionadas = []
    
    if modalidad == 'general':
        tiempo_minutos = int(request.form.get('tiempo'))
        
        # 1. Configuración de límites según tu solicitud
        config_preguntas = {15: 12, 30: 25, 60: 50, 180: 140}
        total_objetivo = config_preguntas.get(tiempo_minutos, 12)
        
        # 2. Pesos oficiales para el cálculo proporcional
        pesos = {
            'Matemáticas': 37/140, 'Competencia Escrita': 20/140,
            'Competencia Lectora': 20/140, 'Química': 17/140,
            'Física': 17/140, 'Historia': 10/140,
            'Inglés': 10/140, 'Biología': 9/140
        }

        # 3. ASEGURAR MÍNIMO 1 POR MATERIA (Si existe en la DB)
        materias_en_db = [m[0] for m in db.session.query(Pregunta.materia).distinct().all()]
        for mat in materias_en_db:
            p = Pregunta.query.filter_by(materia=mat).order_by(db.func.random()).first()
            if p:
                preguntas_seleccionadas.append(p)

        # 4. RELLENO PROPORCIONAL
        # Intentamos llenar según el peso de cada materia
        for materia, peso in pesos.items():
            if len(preguntas_seleccionadas) >= total_objetivo: break
            
            cant_ideal = max(1, int(total_objetivo * peso))
            actuales = len([p for p in preguntas_seleccionadas if p.materia == materia])
            
            if actuales < cant_ideal:
                faltantes_materia = cant_ideal - actuales
                ids_ya_usados = [p.id for p in preguntas_seleccionadas]
                
                extras = Pregunta.query.filter(
                    Pregunta.materia == materia,
                    ~Pregunta.id.in_(ids_ya_usados)
                ).order_by(db.func.random()).limit(faltantes_materia).all()
                
                preguntas_seleccionadas.extend(extras)

        # 5. RELLENO DE EMERGENCIA (Si faltan para llegar al total_objetivo)
        while len(preguntas_seleccionadas) < total_objetivo:
            ids_ya_usados = [p.id for p in preguntas_seleccionadas]
            p_emergencia = Pregunta.query.filter(~Pregunta.id.in_(ids_ya_usados)).order_by(db.func.random()).first()
            if not p_emergencia: break # Se acabaron las preguntas en la DB
            preguntas_seleccionadas.append(p_emergencia)

    elif modalidad == 'materia':
        # (Se mantiene tu lógica de materia individual)
        materia_elegida = request.form.get('materia')
        cantidad = int(request.form.get('cantidad'))
        tiempo_minutos = int(cantidad * 1.5) 
        preguntas_seleccionadas = Pregunta.query.filter_by(materia=materia_elegida).order_by(db.func.random()).limit(cantidad).all()
    
    random.shuffle(preguntas_seleccionadas)
    return render_template('examen.html', preguntas=preguntas_seleccionadas, modalidad=modalidad, tiempo_minutos=tiempo_minutos)



# Única versión de /calificar con la lógica para las gráficas
@app.route('/calificar', methods=['POST'])
def calificar():
    datos_formulario = request.form
    
    # NUEVO: Obtenemos la lista de todas las preguntas que salieron en el examen
    lista_ids = request.form.getlist('preguntas_ids')
    total_preguntas = len(lista_ids)
    aciertos = 0
    
    areas_mejora = {}
    estadisticas_materias = {}

    # Iteramos sobre la lista de IDs del examen, NO sobre lo que mandó el formulario
    for id_str in lista_ids:
        pregunta_id = int(id_str)
        
        # Buscamos la respuesta del usuario. Si no contestó, devuelve None.
        respuesta_usuario = datos_formulario.get(f'resp_{pregunta_id}')
        vio_ayuda = datos_formulario.get(f'ayuda_vista_{pregunta_id}', '0')
        
        pregunta_db = db.session.get(Pregunta, pregunta_id)
        
        if pregunta_db: # Por seguridad, verificamos que la pregunta exista
            materia = pregunta_db.materia
            
            if materia not in estadisticas_materias:
                estadisticas_materias[materia] = {'total': 0, 'aciertos': 0}
            
            estadisticas_materias[materia]['total'] += 1
            
            # Evaluamos si la respuesta es correcta
            es_correcta = (respuesta_usuario == pregunta_db.respuesta_correcta)
            
            if es_correcta and vio_ayuda == '0':
                aciertos += 1
                estadisticas_materias[materia]['aciertos'] += 1
            else:
                # Si se equivocó, usó ayuda, o LA DEJÓ EN BLANCO (respuesta_usuario is None)
                if materia not in areas_mejora:
                    areas_mejora[materia] = 0
                areas_mejora[materia] += 1

    # Calculamos la calificación basada en el total REAL de preguntas del examen
    calificacion_escala_10 = (aciertos / total_preguntas) * 10 if total_preguntas > 0 else 0
    porcentaje = (aciertos / total_preguntas) * 100 if total_preguntas > 0 else 0

    nombres_materias = list(estadisticas_materias.keys())
    puntajes_radar = []
    for mat in nombres_materias:
        tot = estadisticas_materias[mat]['total']
        aci = estadisticas_materias[mat]['aciertos']
        porcentaje_mat = (aci / tot) * 100 if tot > 0 else 0
        puntajes_radar.append(round(porcentaje_mat, 1))

    return render_template(
        'resultados.html', 
        aciertos=aciertos, 
        total=total_preguntas, 
        porcentaje=round(porcentaje, 1),
        calificacion=round(calificacion_escala_10, 1),
        areas_mejora=areas_mejora,
        nombres_materias=json.dumps(nombres_materias),
        puntajes_radar=json.dumps(puntajes_radar)
    )


@app.route('/guardar_procedimiento', methods=['POST'])
def guardar_procedimiento():
    data = request.json
    pregunta_id = data.get('id')
    nuevo_procedimiento = data.get('procedimiento')
    
    pregunta = Pregunta.query.get(pregunta_id)
    if pregunta:
        pregunta.procedimiento = nuevo_procedimiento
        db.session.commit()
        return {"status": "success"}, 200
    return {"status": "error"}, 400



if __name__ == '__main__':
    app.run(debug=True)