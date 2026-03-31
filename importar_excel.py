import csv
from app import app, db, Pregunta

def importar_desde_csv(nombre_archivo):
    # Activamos la base de datos de Flask
    with app.app_context():
        contador = 0
        
        try:
            # Abrimos el archivo CSV
            with open(nombre_archivo, mode='r', encoding='utf-8-sig') as archivo:
                # DictReader convierte cada fila de Excel en un diccionario usando los encabezados
                lector_csv = csv.DictReader(archivo)
                
                for fila in lector_csv:
                    # Validamos que no se repitan las preguntas en la base de datos
                    existe = Pregunta.query.filter_by(texto_pregunta=fila['texto_pregunta']).first()
                    
                    if not existe:
                        nueva_pregunta = Pregunta(
                            materia=fila['materia'],
                            texto_pregunta=fila['texto_pregunta'],
                            imagen=fila.get('imagen', None) if fila.get('imagen') != '' else None,
                            opcion_a=fila['opcion_a'],
                            opcion_b=fila['opcion_b'],
                            opcion_c=fila['opcion_c'],
                            opcion_d=fila['opcion_d'],
                            respuesta_correcta=fila['respuesta_correcta'],
                            # Si la celda de procedimiento está vacía, guarda None
                            procedimiento=fila['procedimiento'] if fila['procedimiento'] else None
                        )
                        db.session.add(nueva_pregunta)
                        contador += 1
                
                # Guardamos todas las filas en SQLite de un solo golpe
                db.session.commit()
                print(f"¡Éxito! Se importaron {contador} preguntas desde {nombre_archivo}")
                
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{nombre_archivo}'. Asegúrate de guardarlo en esta carpeta.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

if __name__ == '__main__':
    # Ejecutamos la función apuntando al archivo que exportaste de Excel
    importar_desde_csv('preguntas.csv')