import csv
from app import app, db, Lectura, PreguntaLectura

def sincronizar_lecturas(csv_lecturas):
    with app.app_context():
        print(f"\n📚 Iniciando sincronización de LECTURAS con: {csv_lecturas}")
        actualizadas = 0
        nuevas = 0
        
        try:
            with open(csv_lecturas, mode='r', encoding='utf-8-sig') as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    try:
                        id_lec = int(fila['id_lectura'])
                    except (ValueError, KeyError):
                        continue
                        
                    lectura_db = db.session.get(Lectura, id_lec)
                    
                    # Leemos la materia (si no viene en el CSV, asumimos Español)
                    materia = fila.get('materia', 'Competencia Lectora').strip()
                    titulo = fila.get('titulo', '').strip()
                    texto = fila.get('texto_lectura', '').strip()
                    imagenes = (fila.get('imagenes') or '').strip() or None
                    referencia = (fila.get('referencia') or '').strip() or None
                    
                    if lectura_db:
                        hay_cambios = False
                        if lectura_db.materia != materia:
                            lectura_db.materia = materia; hay_cambios = True
                        if lectura_db.titulo != titulo:
                            lectura_db.titulo = titulo; hay_cambios = True
                        if lectura_db.texto_lectura != texto:
                            lectura_db.texto_lectura = texto; hay_cambios = True
                        if lectura_db.imagenes != imagenes:
                            lectura_db.imagenes = imagenes; hay_cambios = True
                        if lectura_db.referencia != referencia:
                            lectura_db.referencia = referencia; hay_cambios = True
                            
                        if hay_cambios:
                            actualizadas += 1
                            print(f"   ✏️  Lectura ID {id_lec} ({materia}) modificada.")
                    else:
                        nueva_lec = Lectura(
                            id=id_lec, materia=materia, titulo=titulo, 
                            texto_lectura=texto, imagenes=imagenes, referencia=referencia
                        )
                        db.session.add(nueva_lec)
                        nuevas += 1
                        print(f"   ✨ Lectura ID {id_lec} ({materia}) agregada (Nueva).")
            
            db.session.commit()
            print(f"✅ Lecturas listas: {actualizadas} actualizadas, {nuevas} nuevas.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error en lecturas: {e}")


def sincronizar_preguntas_lectura(csv_preguntas, id_inicio):
    with app.app_context():
        print(f"\n📝 Iniciando sincronización de PREGUNTAS con: {csv_preguntas} (Iniciando en ID {id_inicio})")
        actualizadas = 0
        nuevas = 0
        
        try:
            with open(csv_preguntas, mode='r', encoding='utf-8-sig') as f:
                lector = csv.DictReader(f)
                
                # Usamos enumerate con el id_inicio para asignar los IDs correctos automáticamente
                for i, fila in enumerate(lector, start=id_inicio):
                    id_preg = i 
                    
                    pregunta_db = db.session.get(PreguntaLectura, id_preg)
                    
                    id_lectura = int(fila.get('id_lectura', 0))
                    nivel = fila.get('nivel', 'Superior').strip()
                    texto = fila.get('texto_pregunta', '').strip()
                    imagen = (fila.get('imagen') or '').strip() or None
                    op_a = fila.get('opcion_a', '').strip()
                    op_b = fila.get('opcion_b', '').strip()
                    op_c = fila.get('opcion_c', '').strip()
                    op_d = fila.get('opcion_d', '').strip()
                    resp = fila.get('respuesta_correcta', '').strip()
                    proc = (fila.get('procedimiento') or '').strip() or None
                    
                    if pregunta_db:
                        hay_cambios = False
                        if pregunta_db.id_lectura != id_lectura:
                            pregunta_db.id_lectura = id_lectura; hay_cambios = True
                        if pregunta_db.nivel != nivel:
                            pregunta_db.nivel = nivel; hay_cambios = True
                        if pregunta_db.texto_pregunta != texto:
                            pregunta_db.texto_pregunta = texto; hay_cambios = True
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
                            
                        if hay_cambios:
                            actualizadas += 1
                            print(f"   ✏️  Pregunta ID {id_preg} modificada.")
                    else:
                        nueva_preg = PreguntaLectura(
                            id=id_preg, id_lectura=id_lectura, nivel=nivel,
                            texto_pregunta=texto, imagen=imagen,
                            opcion_a=op_a, opcion_b=op_b, opcion_c=op_c,
                            opcion_d=op_d, respuesta_correcta=resp, procedimiento=proc
                        )
                        db.session.add(nueva_preg)
                        nuevas += 1
                        print(f"   ✨ Pregunta ID {id_preg} agregada (Nueva).")
            
            db.session.commit()
            print(f"✅ Preguntas listas: {actualizadas} actualizadas, {nuevas} nuevas.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error en preguntas de lectura: {e}")

if __name__ == '__main__':
    # 1. Sincronizamos Competencia Lectora (Español)
    sincronizar_lecturas('lecturas_corregido.csv')
    sincronizar_preguntas_lectura('preguntas_lectura_corregido.csv', id_inicio=1)
    
    # 2. Sincronizamos Reading Comprehension (Inglés)
    sincronizar_lecturas('lecturas_ingles.csv')
    sincronizar_preguntas_lectura('preguntas_ingles.csv', id_inicio=1000)