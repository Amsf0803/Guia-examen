from app import app, db, Pregunta

# Lista de diccionarios con las preguntas a inyectar
banco_preguntas = [
    {
        "materia": "Química",
        "texto_pregunta": "Calcular el peso equivalente del carbonato de sodio (Na2CO3).",
        "opcion_a": "21 g/eq",
        "opcion_b": "26 g/eq",
        "opcion_c": "35 g/eq",
        "opcion_d": "53 g/eq",
        "respuesta_correcta": "D",
        "procedimiento": "1. Calculamos el peso molecular del Na2CO3: Na(23x2) + C(12) + O(16x3) = 46 + 12 + 48 = 106 g/mol.\n2. El peso equivalente de una sal se calcula dividiendo el peso molecular entre la carga total del catión (en este caso el Na tiene valencia +1, por 2 átomos = 2).\n3. 106 / 2 = 53 g/eq."
    },
    {
        "materia": "Física",
        "texto_pregunta": "De acuerdo con la Primera Ley de la Termodinámica, si a un sistema se le suministran 500 J de calor y realiza un trabajo de 200 J, ¿cuál es la variación de su energía interna?",
        "opcion_a": "300 J",
        "opcion_b": "700 J",
        "opcion_c": "-300 J",
        "opcion_d": "2.5 J",
        "respuesta_correcta": "A",
        "procedimiento": "La fórmula de la primera ley es: ΔU = Q - W. Donde Q es el calor suministrado (500 J) y W es el trabajo realizado por el sistema (200 J). Por lo tanto: ΔU = 500 J - 200 J = 300 J."
    },
    {
        "materia": "Matemáticas",
        "texto_pregunta": "¿Cuál es la derivada de la función f(x) = 3x^4 - 2x^2 + 5?",
        "opcion_a": "12x^3 - 4x",
        "opcion_b": "12x^4 - 4x^2",
        "opcion_c": "3x^3 - 2x",
        "opcion_d": "12x^3 - 4x + 5",
        "respuesta_correcta": "A",
        "procedimiento": "Utilizamos la regla de la potencia: d/dx (ax^n) = a*n*x^(n-1). \nPara 3x^4: 3*4*x^3 = 12x^3.\nPara -2x^2: -2*2*x^1 = -4x.\nLa derivada de una constante (5) es 0. \nResultado: 12x^3 - 4x."
    },
    {
        "materia": "Competencia Escrita",
        "texto_pregunta": "Selecciona la opción que presenta un error de ortografía:",
        "opcion_a": "Decisión",
        "opcion_b": "Excepción",
        "opcion_c": "Convección",
        "opcion_d": "Extención",
        "respuesta_correcta": "D",
        "procedimiento": "La palabra correcta es 'Extensión', ya que proviene de la familia léxica de palabras terminadas en 'so', 'sor', 'sivo' (extenso, extensor)."
    },
    {
        "materia": "Historia",
        "texto_pregunta": "¿Qué presidente de México impulsó la creación del Instituto Politécnico Nacional (IPN)?",
        "opcion_a": "Plutarco Elías Calles",
        "opcion_b": "Lázaro Cárdenas del Río",
        "opcion_c": "Manuel Ávila Camacho",
        "opcion_d": "Emiliano Zapata",
        "respuesta_correcta": "B",
        "procedimiento": "El IPN fue fundado en 1936 durante el sexenio del presidente Lázaro Cárdenas del Río, en conjunto con Juan de Dios Bátiz."
    }
]

def inyectar_datos():
    # Activamos el contexto de la aplicación Flask para poder usar la BD
    with app.app_context():
        contador = 0
        for p_data in banco_preguntas:
            # Verificamos que la pregunta no exista ya para no duplicar
            existe = Pregunta.query.filter_by(texto_pregunta=p_data['texto_pregunta']).first()
            
            if not existe:
                nueva_p = Pregunta(
                    materia=p_data['materia'],
                    texto_pregunta=p_data['texto_pregunta'],
                    opcion_a=p_data['opcion_a'],
                    opcion_b=p_data['opcion_b'],
                    opcion_c=p_data['opcion_c'],
                    opcion_d=p_data['opcion_d'],
                    respuesta_correcta=p_data['respuesta_correcta'],
                    procedimiento=p_data['procedimiento']
                )
                db.session.add(nueva_p)
                contador += 1
                
        # Guardamos todos los cambios
        db.session.commit()
        print(f"¡Éxito! Se inyectaron {contador} preguntas nuevas a simulador.db")

if __name__ == '__main__':
    inyectar_datos()