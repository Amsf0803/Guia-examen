import csv
import os

csv_path = '/home/amsf08/Codigos/Guia-ipn/respaldo_preguntas.csv'
temp_path = '/home/amsf08/Codigos/Guia-ipn/scratch/respaldo_preguntas_temp.csv'

def get_materia(id_val):
    if 1 <= id_val <= 39:
        return 'Matemáticas_R'
    elif 40 <= id_val <= 78:
        return 'Matemáticas_A'
    elif 79 <= id_val <= 115:
        return 'Matemáticas_T'
    elif 116 <= id_val <= 155:
        return 'Matemáticas_G'
    elif 156 <= id_val <= 195:
        return 'Matemáticas_D'
    elif 196 <= id_val <= 236:
        return 'Matemáticas_I'
    elif 237 <= id_val <= 273:
        return 'Matemáticas_P'
    return None

with open(csv_path, 'r', encoding='utf-8') as f_in, open(temp_path, 'w', encoding='utf-8', newline='') as f_out:
    reader = csv.reader(f_in)
    writer = csv.writer(f_out)
    
    header = next(reader)
    writer.writerow(header)
    
    for row in reader:
        try:
            row_id = int(row[0])
            new_materia = get_materia(row_id)
            if new_materia:
                row[2] = new_materia
        except Exception:
            pass
        writer.writerow(row)

os.replace(temp_path, csv_path)
print("CSV actualizado con éxito.")
