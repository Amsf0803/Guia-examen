import csv
from app import app, db, Lectura, PreguntaLectura

def importar_ingles(csv_lecturas, csv_preguntas):
    with app.app_context():
        # --- 1. IMPORTAR LECTURAS DE INGLÉS ---
        try:
            with open(csv_lecturas, mode='r', encoding='utf-8-sig') as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    id_lec = int(fila['id_lectura'])
                    existe = db.session.get(Lectura, id_lec)
                    
                    if not existe:
                        nueva_lectura = Lectura(
                            id=id_lec,
                            materia=fila.get('materia', 'Inglés').strip(),
                            titulo=fila['titulo'].strip(),
                            texto_lectura=fila['texto_lectura'].strip(),
                            imagenes=(fila.get('imagenes') or '').strip() or None,
                            referencia=(fila.get('referencia') or '').strip() or None 
                        )
                        db.session.add(nueva_lectura)
            db.session.commit()
            print("✅ Lecturas de Inglés importadas correctamente.")
        except Exception as e:
            print(f"❌ Error al importar lecturas de inglés: {e}")

        # --- 2. IMPORTAR PREGUNTAS DE INGLÉS (EMPEZANDO EN ID 1000) ---
        try:
            with open(csv_preguntas, mode='r', encoding='utf-8-sig') as archivo:
                lector = csv.DictReader(archivo)
                id_seguro = 1000  # Empezamos desde el 1000 para no chocar con las de Español
                
                for fila in lector:
                    texto = (fila.get('texto_pregunta') or '').strip()
                    if not texto: continue
                    
                    existe = db.session.get(PreguntaLectura, id_seguro)
                    if not existe:
                        nueva_pregunta = PreguntaLectura(
                            id=id_seguro,
                            id_lectura=int(fila['id_lectura']),
                            nivel=(fila.get('nivel') or 'Superior').strip(),
                            texto_pregunta=texto,
                            imagen=(fila.get('imagen') or '').strip() or None,
                            opcion_a=(fila.get('opcion_a') or '').strip(),
                            opcion_b=(fila.get('opcion_b') or '').strip(),
                            opcion_c=(fila.get('opcion_c') or '').strip(),
                            opcion_d=(fila.get('opcion_d') or '').strip(),
                            respuesta_correcta=(fila.get('respuesta_correcta') or '').strip(),
                            procedimiento=None
                        )
                        db.session.add(nueva_pregunta)
                    
                    id_seguro += 1 # Aumentamos el ID para la siguiente pregunta
                    
            db.session.commit()
            print("✅ Preguntas de Inglés importadas correctamente (IDs del 1000 en adelante).")
        except Exception as e:
            print(f"❌ Error al importar preguntas: {e}")

if __name__ == '__main__':
    # Pon los nombres exactos de los archivos que me enviaste
    importar_ingles('lecturas_ingles.csv', 'preguntas_ingles.csv')