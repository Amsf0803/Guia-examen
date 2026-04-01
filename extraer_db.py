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
                SELECT id, materia, texto_pregunta, imagen, opcion_a, opcion_b, 
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
                    'id', 'nivel', 'materia', 'texto_pregunta', 'imagen', 
                    'opcion_a', 'opcion_b', 'opcion_c', 'opcion_d', 
                    'respuesta_correcta', 'procedimiento'
                ])
                
                for p in preguntas:
                    # 'p' es una tupla con los resultados de nuestra consulta SQL
                    escritor.writerow([
                        p[0],        # id
                        'Superior',  # Inyectamos el nivel manualmente
                        p[1],        # materia
                        p[2],        # texto_pregunta
                        p[3] if p[3] else '', 
                        p[4], 
                        p[5], 
                        p[6], 
                        p[7], 
                        p[8], 
                        p[9] if p[9] else ''
                    ])
                    
            print(f"✅ ¡Rescate exitoso! Se guardaron {len(preguntas)} preguntas en '{csv_file}'.")
            
        except Exception as e:
            print(f"❌ Error al leer la base de datos: {e}")

if __name__ == '__main__':
    exportar_raw_sqlalchemy()