from app import app, db, Pregunta

def arreglar_angulos():
    with app.app_context():
        # 1. Buscamos las preguntas marcadas con la palabra "angulo"
        preguntas_marcadas = Pregunta.query.filter(Pregunta.procedimiento.like('%angulo%')).all()
        
        if not preguntas_marcadas:
            print("No se encontró ninguna pregunta con la palabra 'angulo' en el procedimiento.")
            return

        print(f"Se encontraron {len(preguntas_marcadas)} pregunta(s) para corregir.")
        
        # 2. Iteramos sobre ellas para corregir el LaTeX
        for p in preguntas_marcadas:
            print(f"- Corrigiendo pregunta ID {p.id} (Materia: {p.materia})")
            
            # Reemplazamos los errores en la pregunta principal
            if p.texto_pregunta:
                p.texto_pregunta = p.texto_pregunta.replace(r'\angleA', r'\angle A')
                p.texto_pregunta = p.texto_pregunta.replace(r'\angleB', r'\angle B')
            
            # Por precaución, también revisamos si el error se coló en las opciones
            if p.opcion_a: p.opcion_a = p.opcion_a.replace(r'\angleA', r'\angle A').replace(r'\angleB', r'\angle B')
            if p.opcion_b: p.opcion_b = p.opcion_b.replace(r'\angleA', r'\angle A').replace(r'\angleB', r'\angle B')
            if p.opcion_c: p.opcion_c = p.opcion_c.replace(r'\angleA', r'\angle A').replace(r'\angleB', r'\angle B')
            if p.opcion_d: p.opcion_d = p.opcion_d.replace(r'\angleA', r'\angle A').replace(r'\angleB', r'\angle B')
            
            # 3. Borramos la marca "angulo" del procedimiento dejándolo vacío
            p.procedimiento = None 
            
        # 4. Guardamos los cambios en la base de datos
        db.session.commit()
        print("\n¡Corrección de ángulos completada con éxito!")

if __name__ == '__main__':
    arreglar_angulos()