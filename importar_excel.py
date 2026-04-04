import csv
from app import app, db, Pregunta

def importar_desde_csv(nombre_archivo):
    # Activamos la base de datos de Flask
    with app.app_context():
        contador_importadas = 0
        
        try:
            # Abrimos el archivo CSV
            with open(nombre_archivo, mode='r', encoding='utf-8-sig') as archivo:
                lector_csv = csv.DictReader(archivo)
                
                for i, fila in enumerate(lector_csv, start=1):
                    # Usamos (valor or '') para evitar el error de 'NoneType'
                    texto = (fila.get('texto_pregunta') or '').strip()
                    
                    # Ignorar filas completamente vacías
                    if not texto:
                        continue
                        
                    # ⚠️ SE ELIMINÓ LA VALIDACIÓN DE DUPLICADOS
                    # Todo lo que esté en el CSV se subirá a la base de datos
                    
                    nueva_pregunta = Pregunta(
                        nivel=(fila.get('nivel') or 'Superior').strip(), 
                        materia=(fila.get('materia') or 'Matemáticas').strip(),
                        texto_pregunta=texto,
                        # Si da un string vacío, el "or None" lo convierte en un nulo para SQLite
                        imagen=(fila.get('imagen') or '').strip() or None,
                        opcion_a=(fila.get('opcion_a') or '').strip(),
                        opcion_b=(fila.get('opcion_b') or '').strip(),
                        opcion_c=(fila.get('opcion_c') or '').strip(),
                        opcion_d=(fila.get('opcion_d') or '').strip(),
                        respuesta_correcta=(fila.get('respuesta_correcta') or '').strip(),
                        procedimiento=(fila.get('procedimiento') or '').strip() or None
                    )
                    db.session.add(nueva_pregunta)
                    contador_importadas += 1
                
                # Guardamos todas las filas en SQLite
                db.session.commit()
                print("\n" + "="*40)
                print(f"✅ ¡Éxito! Se importaron {contador_importadas} preguntas.")
                print("="*40 + "\n")
                
        except FileNotFoundError:
            print(f"❌ Error: No se encontró el archivo '{nombre_archivo}'.")
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado en la fila {i}: {e}")

if __name__ == '__main__':
    # Apuntamos directamente al respaldo que acabamos de crear
    importar_desde_csv('respaldo_preguntas.csv')