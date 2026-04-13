import csv
from app import app, db
from sqlalchemy import text

def exportar_raw_sqlalchemy(csv_file='respaldo_preguntas.csv'):
    # Usamos la app de Flask para que él encuentre el archivo de la BD automáticamente
    with app.app_context():
        try:
            # Le pedimos directamente a SQLAlchemy que ejecute SQL crudo 
            # pidiendo SOLO las columnas viejas (así evitamos el error de 'nivel')
            resultado = db.session.execute(text("""
                SELECT id, materia, texto_pregunta, imagen_texto, imagen, opcion_a, opcion_b, 
                       opcion_c, opcion_d, respuesta_correcta, procedimiento 
                FROM pregunta
            """))
            preguntas = resultado.fetchall()
            
            if not preguntas:
                print("La base de datos está vacía. No hay nada que exportar.")
                return
                
            # Abrimos el CSV para guardar
            with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as archivo:
                escritor = csv.writer(archivo)
                
                # Escribimos los encabezados incluyendo la nueva columna 'nivel'
                escritor.writerow([
                    'id', 'nivel', 'materia', 'texto_pregunta', 'imagen_texto', 'imagen', 
                    'opcion_a', 'opcion_b', 'opcion_c', 'opcion_d', 
                    'respuesta_correcta', 'procedimiento'
                ])
                
                for p in preguntas:
                    # 'p' es una tupla con los resultados de nuestra consulta SQL
                    escritor.writerow([
                        p[0],        # id
                        'Superior',  # nivel
                        p[1],        # materia
                        p[2],        # texto_pregunta
                        p[3] if p[3] else '', # imagen_texto
                        p[4] if p[4] else '', # imagen
                        p[5],        # opcion_a
                        p[6],        # opcion_b
                        p[7],        # opcion_c
                        p[8],        # opcion_d
                        p[9],        # respuesta_correcta
                        p[10] if p[10] else '' # procedimiento
                    ])
                    
            print(f"✅ ¡Rescate exitoso! Se guardaron {len(preguntas)} preguntas en '{csv_file}'.")
            
        except Exception as e:
            print(f"❌ Error al leer la base de datos: {e}")

if __name__ == '__main__':
    exportar_raw_sqlalchemy()