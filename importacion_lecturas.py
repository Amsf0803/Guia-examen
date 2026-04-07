import csv
from app import app, db, Lectura, PreguntaLectura

def importar_competencia_lectora(csv_lecturas, csv_preguntas):
    with app.app_context():
        # 1. ¡LA MAGIA ESTÁ AQUÍ! Esto crea las tablas físicas si no existen
        db.create_all()

        # --- 1. IMPORTAR LECTURAS ---
        try:
            with open(csv_lecturas, mode='r', encoding='utf-8-sig') as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    id_lec = int(fila['id_lectura'])
                    
                    # 2. CORRECCIÓN DE LA ADVERTENCIA (Estilo SQLAlchemy 2.0)
                    existe = db.session.get(Lectura, id_lec)
                    
                    if not existe:
                        nueva_lectura = Lectura(
                            id=id_lec,
                            titulo=fila['titulo'].strip(),
                            texto_lectura=fila['texto_lectura'].strip(),
                            imagenes=(fila.get('imagenes') or '').strip() or None,
                            referencia=(fila.get('referencia') or '').strip() or None 
                        )
                        db.session.add(nueva_lectura)
            db.session.commit()
            print("✅ Lecturas importadas correctamente.")
        except Exception as e:
            print(f"❌ Error al importar lecturas: {e}")

        # --- 2. IMPORTAR PREGUNTAS ---
        try:
            with open(csv_preguntas, mode='r', encoding='utf-8-sig') as archivo:
                lector = csv.DictReader(archivo)
                for i, fila in enumerate(lector, start=1):
                    texto = (fila.get('texto_pregunta') or '').strip()
                    if not texto: continue
                    
                    nueva_pregunta = PreguntaLectura(
                        id_lectura=int(fila['id_lectura']),
                        nivel=(fila.get('nivel') or 'Superior').strip(),
                        texto_pregunta=texto,
                        imagen=(fila.get('imagen') or '').strip() or None,
                        opcion_a=(fila.get('opcion_a') or '').strip(),
                        opcion_b=(fila.get('opcion_b') or '').strip(),
                        opcion_c=(fila.get('opcion_c') or '').strip(),
                        opcion_d=(fila.get('opcion_d') or '').strip(),
                        respuesta_correcta=(fila.get('respuesta_correcta') or '').strip()
                    )
                    db.session.add(nueva_pregunta)
            db.session.commit()
            print("✅ Preguntas de lectura importadas correctamente.")
        except Exception as e:
            print(f"❌ Error al importar preguntas en fila {i}: {e}")

if __name__ == '__main__':
    # Apuntamos a los archivos ya corregidos
    importar_competencia_lectora('lecturas_corregido.csv', 'preguntas_lectura_corregido.csv')