from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simulador.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODELO DE LA BASE DE DATOS ---
class Pregunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # NUEVA COLUMNA: Para separar preguntas de prepa y universidad
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

with app.app_context():
    db.create_all()

# ==========================================
# BASE DE DATOS DE ESTUDIO (TEMARIO DIVIDIDO)
# ==========================================
temario_estudio = {
    "Superior": {
        "Matemáticas": [
            {
                "id": "mat_1_1_1",
                "titulo": "1.1.1 Sucesiones numéricas",
                "explicacion": r"""
                <p>Una <strong>sucesión numérica</strong> es un conjunto ordenado de números que siguen una regla o patrón específico. Cada número en la sucesión se llama <em>término</em>.</p>
                <ul>
                    <li><strong>Progresión Aritmética:</strong> La diferencia entre términos consecutivos es constante. Se suma o resta siempre la misma cantidad. Fórmula del término general: $$a_n = a_1 + (n - 1)d$$ donde $a_1$ es el primer término y $d$ es la diferencia.</li>
                    <li><strong>Progresión Geométrica:</strong> La razón entre términos consecutivos es constante. Se multiplica o divide siempre por la misma cantidad. Fórmula: $$a_n = a_1 \cdot r^{n - 1}$$ donde $r$ es la razón.</li>
                </ul>
                """,
                "ejercicios": [
                    {
                        "pregunta": r"¿Cuál es el décimo término de la sucesión: $3, 7, 11, 15, \dots$?",
                        "solucion": r"""
                        <strong>Paso 1:</strong> Identificar el tipo de sucesión. Observamos que $7-3=4$, $11-7=4$. Es una progresión aritmética con diferencia $d = 4$.<br>
                        <strong>Paso 2:</strong> Identificar el primer término: $a_1 = 3$.<br>
                        <strong>Paso 3:</strong> Sustituir en la fórmula general para $n=10$:<br>
                        $$a_{10} = 3 + (10 - 1)(4)$$<br>
                        $$a_{10} = 3 + (9)(4)$$<br>
                        $$a_{10} = 3 + 36 = 39$$<br>
                        <strong>Respuesta:</strong> El décimo término es 39.
                        """
                    },
                    {
                        "pregunta": r"Encuentra el 6° término de la sucesión: $2, 6, 18, 54, \dots$",
                        "solucion": r"""
                        <strong>Paso 1:</strong> Identificar el patrón. Vemos que $6 \div 2 = 3$, $18 \div 6 = 3$. Es una progresión geométrica con razón $r = 3$.<br>
                        <strong>Paso 2:</strong> El primer término es $a_1 = 2$.<br>
                        <strong>Paso 3:</strong> Sustituir en la fórmula para $n=6$:<br>
                        $$a_6 = 2 \cdot (3)^{6 - 1}$$<br>
                        $$a_6 = 2 \cdot (3)^5$$<br>
                        $$a_6 = 2 \cdot 243 = 486$$<br>
                        <strong>Respuesta:</strong> El sexto término es 486.
                        """
                    }
                ]
            },
            {
                "id": "mat_2_2_4",
                "titulo": "2.2.4 Productos Notables",
                "explicacion": r"""
                <p>Los <strong>productos notables</strong> son multiplicaciones de polinomios cuyos resultados pueden obtenerse directamente mediante reglas fijas, sin necesidad de hacer la multiplicación término a término.</p>
                <ul>
                    <li><strong>Binomio al cuadrado:</strong> El cuadrado del primer término, más el doble del primero por el segundo, más el cuadrado del segundo.<br> $$(a \pm b)^2 = a^2 \pm 2ab + b^2$$</li>
                    <li><strong>Binomios conjugados:</strong> El producto de la suma por la diferencia de dos cantidades es igual a una diferencia de cuadrados.<br> $$(a + b)(a - b) = a^2 - b^2$$</li>
                    <li><strong>Binomios con término común:</strong> El cuadrado del común, más la suma de los no comunes por el común, más el producto de los no comunes.<br> $$(x + a)(x + b) = x^2 + (a+b)x + ab$$</li>
                </ul>
                """,
                "ejercicios": [
                    {
                        "pregunta": r"Desarrolla el siguiente binomio al cuadrado: $(3x + 5y)^2$",
                        "solucion": r"""
                        <strong>Paso 1:</strong> Identificar la regla a usar: $(a + b)^2 = a^2 + 2ab + b^2$.<br>
                        <strong>Paso 2:</strong> Asignar valores: $a = 3x$ y $b = 5y$.<br>
                        <strong>Paso 3:</strong> Aplicar la regla:<br>
                        $$(3x)^2 + 2(3x)(5y) + (5y)^2$$<br>
                        <strong>Paso 4:</strong> Simplificar cada término:<br>
                        $$9x^2 + 30xy + 25y^2$$<br>
                        <strong>Respuesta:</strong> $9x^2 + 30xy + 25y^2$
                        """
                    },
                    {
                        "pregunta": r"Resuelve el producto de binomios conjugados: $(4m^2 - 7n)(4m^2 + 7n)$",
                        "solucion": r"""
                        <strong>Paso 1:</strong> Aplicar la regla de diferencia de cuadrados: $(a - b)(a + b) = a^2 - b^2$.<br>
                        <strong>Paso 2:</strong> Aquí $a = 4m^2$ y $b = 7n$.<br>
                        <strong>Paso 3:</strong> Elevar cada término al cuadrado:<br>
                        $$(4m^2)^2 - (7n)^2$$<br>
                        <strong>Paso 4:</strong> Simplificar (recordando multiplicar los exponentes):<br>
                        $$16m^4 - 49n^2$$<br>
                        <strong>Respuesta:</strong> $16m^4 - 49n^2$
                        """
                    }
                ]
            }
        ]
    },
    "Medio Superior": {
        "Matemáticas": [
            {
                "id": "mat_nms_1",
                "titulo": "1.1 Jerarquía de Operaciones (Secundaria)",
                "explicacion": r"""
                <p>La <strong>jerarquía de operaciones</strong> es el orden correcto en el que deben resolverse las operaciones en una expresión matemática.</p>
                <ol>
                    <li>Paréntesis, corchetes y llaves $()$, $[]$, $\{\}$.</li>
                    <li>Potencias y raíces $x^2$, $\sqrt{x}$.</li>
                    <li>Multiplicaciones y divisiones $\times$, $\div$ (de izquierda a derecha).</li>
                    <li>Sumas y restas $+$, $-$ (de izquierda a derecha).</li>
                </ol>
                """,
                "ejercicios": [
                    {
                        "pregunta": r"Resuelve: $5 + 3 \times (8 - 2)^2 \div 4$",
                        "solucion": r"""
                        <strong>Paso 1 (Paréntesis):</strong> $8 - 2 = 6$<br>
                        La expresión queda: $5 + 3 \times (6)^2 \div 4$<br>
                        <strong>Paso 2 (Potencias):</strong> $6^2 = 36$<br>
                        La expresión queda: $5 + 3 \times 36 \div 4$<br>
                        <strong>Paso 3 (Multiplicación y División de izq a der):</strong> $3 \times 36 = 108$, luego $108 \div 4 = 27$<br>
                        La expresión queda: $5 + 27$<br>
                        <strong>Paso 4 (Suma):</strong> $5 + 27 = 32$<br>
                        <strong>Respuesta:</strong> $32$
                        """
                    }
                ]
            }
        ]
    }
}

# --- RUTAS DE LOS MENÚS PRINCIPALES ---
@app.route('/')
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
    temario_nivel = temario_estudio.get(nivel, {})
    url_retorno = "/menu_superior" if nivel == "Superior" else "/menu_medio_superior"
    return render_template('estudio_menu.html', temario=temario_nivel, nivel=nivel, url_retorno=url_retorno)

@app.route('/estudio/<nivel>/<materia>/<tema_id>')
def detalle_estudio(nivel, materia, tema_id):
    temario_nivel = temario_estudio.get(nivel, {})
    if materia in temario_nivel:
        for tema in temario_nivel[materia]:
            if tema['id'] == tema_id:
                url_retorno = f"/estudio/{nivel}"
                return render_template('estudio_detalle.html', materia=materia, tema=tema, nivel=nivel, url_retorno=url_retorno)
    return "Tema no encontrado", 404


@app.route('/agregar_pregunta', methods=['GET', 'POST'])
@app.route('/agregar_pregunta/<nivel>', methods=['GET', 'POST'])
def agregar_pregunta(nivel="Superior"):
    if request.method == 'POST':
        nueva_pregunta = Pregunta(
            nivel=request.form.get('nivel'), 
            materia=request.form.get('materia'),
            texto_pregunta=request.form.get('texto_pregunta'),
            opcion_a=request.form.get('opcion_a'),
            opcion_b=request.form.get('opcion_b'),
            opcion_c=request.form.get('opcion_c'),
            opcion_d=request.form.get('opcion_d'),
            respuesta_correcta=request.form.get('respuesta_correcta'),
            procedimiento=request.form.get('procedimiento')
        )
        db.session.add(nueva_pregunta)
        db.session.commit()
        # Al terminar, redirigimos manteniendo el nivel para seguir agregando del mismo tipo
        return redirect(url_for('agregar_pregunta', nivel=request.form.get('nivel'))) 
    
    # Determinamos a dónde regresar el botón
    url_retorno = url_for('menu_superior') if nivel == "Superior" else url_for('menu_medio_superior')
    
    return render_template('agregar.html', nivel_actual=nivel, url_retorno=url_retorno)

@app.route('/iniciar_examen', methods=['POST'])
def iniciar_examen():
    modalidad = request.form.get('modalidad')
    nivel = request.form.get('nivel', 'Superior')
    preguntas_seleccionadas = []
    
    if modalidad == 'general':
        tiempo_minutos = int(request.form.get('tiempo'))
        config_preguntas = {15: 12, 30: 25, 60: 50, 180: 140}
        total_objetivo = config_preguntas.get(tiempo_minutos, 12)

        pesos = {
            'Matemáticas': 37/140, 'Competencia Escrita': 20/140,
            'Competencia Lectora': 20/140, 'Química': 17/140,
            'Física': 17/140, 'Historia': 10/140,
            'Inglés': 10/140, 'Biología': 9/140,
            'Formación Cívica y Ética': 10/140, 'Español': 20/140 # Agregados para NMS
        }

        # CAMBIO: Ahora TODO filtra por "nivel=nivel"
        materias_en_db = [m[0] for m in db.session.query(Pregunta.materia).filter_by(nivel=nivel).distinct().all()]
        for mat in materias_en_db:
            p = Pregunta.query.filter_by(materia=mat, nivel=nivel).order_by(db.func.random()).first()
            if p:
                preguntas_seleccionadas.append(p)

        for materia, peso in pesos.items():
            if len(preguntas_seleccionadas) >= total_objetivo: break
            cant_ideal = max(1, int(total_objetivo * peso))
            actuales = len([p for p in preguntas_seleccionadas if p.materia == materia])
            if actuales < cant_ideal:
                faltantes_materia = cant_ideal - actuales
                ids_ya_usados = [p.id for p in preguntas_seleccionadas]
                extras = Pregunta.query.filter(
                    Pregunta.materia == materia,
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

    elif modalidad == 'materia':
        materia_elegida = request.form.get('materia')
        cantidad = int(request.form.get('cantidad'))
        tiempo_minutos = int(cantidad * 1.5) 
        # FILTRO DE NIVEL APLICADO AQUÍ TAMBIÉN
        preguntas_seleccionadas = Pregunta.query.filter_by(materia=materia_elegida, nivel=nivel).order_by(db.func.random()).limit(cantidad).all()
    
    random.shuffle(preguntas_seleccionadas)
    return render_template('examen.html', preguntas=preguntas_seleccionadas, modalidad=modalidad, tiempo_minutos=tiempo_minutos, nivel=nivel)

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
        pregunta_id = int(id_str)
        respuesta_usuario = datos_formulario.get(f'resp_{pregunta_id}')
        vio_ayuda = datos_formulario.get(f'ayuda_vista_{pregunta_id}', '0')
        
        pregunta_db = db.session.get(Pregunta, pregunta_id)
        
        if pregunta_db: 
            materia = pregunta_db.materia
            
            if materia not in estadisticas_materias:
                estadisticas_materias[materia] = {'total': 0, 'aciertos': 0}
            
            estadisticas_materias[materia]['total'] += 1
            
            es_correcta = (respuesta_usuario == pregunta_db.respuesta_correcta)
            en_blanco = (respuesta_usuario is None)
            
            if es_correcta and vio_ayuda == '0':
                aciertos += 1
                estadisticas_materias[materia]['aciertos'] += 1
            else:
                if materia not in areas_mejora:
                    areas_mejora[materia] = 0
                areas_mejora[materia] += 1

            # NUEVO: Guardamos toda la info de esta pregunta para la revisión
            detalles_examen.append({
                'pregunta': pregunta_db,
                'respuesta_usuario': respuesta_usuario,
                'es_correcta': es_correcta and vio_ayuda == '0',
                'en_blanco': en_blanco
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
    pregunta_id = data.get('id')
    nuevo_procedimiento = data.get('procedimiento')

    pregunta = Pregunta.query.get(pregunta_id)
    if pregunta:
        pregunta.procedimiento = nuevo_procedimiento
        db.session.commit()
        print(f"¡Procedimiento guardado para la pregunta {pregunta_id}!") # Agrega este print para depurar
        return {"status": "success"}, 200
    return {"status": "error"}, 400




if __name__ == '__main__':
    app.run(debug=True)