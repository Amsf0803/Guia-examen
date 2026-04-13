import csv
from app import app, db, Pregunta

def sincronizar_preguntas(archivo_csv):
    with app.app_context():
        print(f"🔄 Iniciando sincronización con el archivo: {archivo_csv}...")
        
        preguntas_actualizadas = 0
        preguntas_nuevas = 0
        
        try:
            with open(archivo_csv, mode='r', encoding='utf-8-sig') as f:
                lector = csv.DictReader(f)
                
                for fila in lector:
                    try:
                        # Obtener el ID del CSV
                        id_csv = int(fila['id'])
                    except (ValueError, KeyError):
                        continue # Si la fila no tiene un ID válido, la saltamos
                        
                    # 1. Buscamos la pregunta en la Base de Datos
                    pregunta_db = db.session.get(Pregunta, id_csv)
                    
                    # 2. Extraemos y limpiamos los datos del CSV
                    nivel = fila.get('nivel', 'Superior').strip()
                    materia = fila.get('materia', '').strip()
                    texto = fila.get('texto_pregunta', '').strip()
                    img_txt = (fila.get('imagen_texto') or '').strip() or None
                    imagen = (fila.get('imagen') or '').strip() or None
                    op_a = fila.get('opcion_a', '').strip()
                    op_b = fila.get('opcion_b', '').strip()
                    op_c = fila.get('opcion_c', '').strip()
                    op_d = fila.get('opcion_d', '').strip()
                    resp = fila.get('respuesta_correcta', '').strip()
                    proc = (fila.get('procedimiento') or '').strip() or None
                    
                    if pregunta_db:
                        # 3. SI EXISTE: Comparamos para ver si hay cambios
                        hay_cambios = False
                        
                        if pregunta_db.nivel != nivel:
                            pregunta_db.nivel = nivel; hay_cambios = True
                        if pregunta_db.materia != materia:
                            pregunta_db.materia = materia; hay_cambios = True
                        if pregunta_db.texto_pregunta != texto:
                            pregunta_db.texto_pregunta = texto; hay_cambios = True
                        if getattr(pregunta_db, 'imagen_texto', None) != img_txt:
                            pregunta_db.imagen_texto = img_txt; hay_cambios = True
                        if pregunta_db.imagen != imagen:
                            pregunta_db.imagen = imagen; hay_cambios = True
                        if pregunta_db.opcion_a != op_a:
                            pregunta_db.opcion_a = op_a; hay_cambios = True
                        if pregunta_db.opcion_b != op_b:
                            pregunta_db.opcion_b = op_b; hay_cambios = True
                        if pregunta_db.opcion_c != op_c:
                            pregunta_db.opcion_c = op_c; hay_cambios = True
                        if pregunta_db.opcion_d != op_d:
                            pregunta_db.opcion_d = op_d; hay_cambios = True
                        if pregunta_db.respuesta_correcta != resp:
                            pregunta_db.respuesta_correcta = resp; hay_cambios = True
                        if pregunta_db.procedimiento != proc:
                            pregunta_db.procedimiento = proc; hay_cambios = True
                            
                        # Si encontramos alguna diferencia, la contamos como actualizada
                        if hay_cambios:
                            preguntas_actualizadas += 1
                            print(f"✏️  Pregunta ID {id_csv} modificada/corregida.")
                            
                    else:
                        # 4. SI NO EXISTE: Es una pregunta totalmente nueva, la agregamos
                        nueva_pregunta = Pregunta(
                            id=id_csv,
                            nivel=nivel,
                            materia=materia,
                            texto_pregunta=texto,
                            imagen_texto=img_txt,
                            imagen=imagen,
                            opcion_a=op_a,
                            opcion_b=op_b,
                            opcion_c=op_c,
                            opcion_d=op_d,
                            respuesta_correcta=resp,
                            procedimiento=proc
                        )
                        db.session.add(nueva_pregunta)
                        preguntas_nuevas += 1
                        print(f"✨ Pregunta ID {id_csv} agregada a la BD (Nueva).")
            
            # 5. Guardar todos los cambios de golpe al final
            db.session.commit()
            
            print("\n✅ ¡Sincronización completada con éxito!")
            print(f"📊 Resumen de la operación:")
            print(f"   - Preguntas actualizadas: {preguntas_actualizadas}")
            print(f"   - Preguntas nuevas agregadas: {preguntas_nuevas}")
            print("🔒 Seguridad: Ninguna pregunta fue eliminada de la Base de Datos.")
            
        except Exception as e:
            db.session.rollback() # Si algo sale catastróficamente mal, deshacemos todo
            print(f"❌ Error al procesar el archivo: {e}")

if __name__ == '__main__':
    # Pon aquí el nombre exacto de tu archivo CSV (ej. 'respaldo_archivos.csv')
    sincronizar_preguntas('respaldo_preguntas.csv')
    sincronizar_preguntas('historia_superior.csv') 
    sincronizar_preguntas('biologia_superior.csv')
    sincronizar_preguntas('quimica_ingenieria_corregido.csv')
    sincronizar_preguntas('fisica_ingenieria_corregido.csv')
    
