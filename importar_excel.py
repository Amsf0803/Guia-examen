import csv
from app import app, db, Pregunta

def importar_desde_csv(nombre_archivo):
    # Activamos la base de datos de Flask
    with app.app_context():
        contador_importadas = 0
        contador_omitidas = 0
        
        try:
            # Abrimos el archivo CSV
            with open(nombre_archivo, mode='r', encoding='utf-8-sig') as archivo:
                lector_csv = csv.DictReader(archivo)
                
                for i, fila in enumerate(lector_csv, start=1):
                    texto = fila.get('texto_pregunta', '').strip()
                    
                    # Ignorar filas completamente vacías
                    if not texto:
                        continue
                        
                    # Validamos que no se repitan las preguntas
                    existe = Pregunta.query.filter_by(texto_pregunta=texto).first()
                    
                    if not existe:
                        nueva_pregunta = Pregunta(
                            # NUEVO: Ahora leemos y guardamos el nivel (por defecto 'Superior')
                            nivel=fila.get('nivel', 'Superior'), 
                            materia=fila.get('materia', 'Matemáticas'),
                            texto_pregunta=texto,
                            imagen=fila.get('imagen', None) if fila.get('imagen', '').strip() != '' else None,
                            opcion_a=fila.get('opcion_a', ''),
                            opcion_b=fila.get('opcion_b', ''),
                            opcion_c=fila.get('opcion_c', ''),
                            opcion_d=fila.get('opcion_d', ''),
                            respuesta_correcta=fila.get('respuesta_correcta', ''),
                            procedimiento=fila.get('procedimiento', None) if fila.get('procedimiento', '').strip() != '' else None
                        )
                        db.session.add(nueva_pregunta)
                        contador_importadas += 1
                    else:
                        print(f"⚠️ Fila {i} omitida (ya existe en BD): {texto[:50]}...")
                        contador_omitidas += 1
                
                # Guardamos todas las filas en SQLite
                db.session.commit()
                print("\n" + "="*40)
                print(f"✅ ¡Éxito! Se importaron {contador_importadas} preguntas nuevas al Nivel Superior.")
                if contador_omitidas > 0:
                    print(f"⚠️ Se omitieron {contador_omitidas} preguntas porque ya existían.")
                print("="*40 + "\n")
                
        except FileNotFoundError:
            print(f"❌ Error: No se encontró el archivo '{nombre_archivo}'.")
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado en la fila {i}: {e}")

if __name__ == '__main__':
    # Apuntamos directamente al respaldo que acabamos de crear
    importar_desde_csv('respaldo_preguntas.csv')