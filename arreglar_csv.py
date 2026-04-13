"""
Esto es para quimica
import pandas as pd

# Leemos el archivo que te dio la IA
df = pd.read_csv('quimica_ingenieria.csv')

# 1. Renumerar IDs empezando desde el 3000
df['id'] = range(3000, 3000 + len(df))

# 2. Renumerar imágenes empezando desde 58
contador_img = 58
img_cols = ['imagen', 'opcion_a', 'opcion_b', 'opcion_c', 'opcion_d']

for i, row in df.iterrows():
    # Revisar si la fila tiene alguna imagen
    tiene_imagen = False
    for col in img_cols:
        if pd.notna(row[col]) and '.png' in str(row[col]).lower():
            tiene_imagen = True
            break
            
    if tiene_imagen:
        # Reemplazar con el nuevo contador
        if pd.notna(row['imagen']) and '.png' in str(row['imagen']).lower():
            df.at[i, 'imagen'] = f"p{contador_img}.png"
            
        for col, letra in zip(['opcion_a', 'opcion_b', 'opcion_c', 'opcion_d'], ['a', 'b', 'c', 'd']):
            if pd.notna(row[col]) and '.png' in str(row[col]).lower():
                df.at[i, col] = f"{letra}{contador_img}.png"
                
        contador_img += 1

# Guardar el CSV corregido con todas las comillas obligatorias
df.to_csv('quimica_ingenieria_corregido.csv', index=False, quoting=1)
print("¡Archivo corregido! Guardado como 'quimica_ingenieria_corregido.csv'.")

"""

#Esto es para fisica:

import pandas as pd

# Leemos el archivo que te dio la IA
df = pd.read_csv('fisica_ingenieria.csv')

# 1. Renumerar IDs empezando desde el 4000 para Física
df['id'] = range(4000, 4000 + len(df))

# 2. Renumerar imágenes empezando desde el 66
contador_img = 66
img_cols = ['imagen', 'opcion_a', 'opcion_b', 'opcion_c', 'opcion_d']

for i, row in df.iterrows():
    # Revisar si la fila tiene alguna imagen
    tiene_imagen = False
    for col in img_cols:
        if pd.notna(row[col]) and '.png' in str(row[col]).lower():
            tiene_imagen = True
            break
            
    if tiene_imagen:
        # Reemplazar con el nuevo contador
        if pd.notna(row['imagen']) and '.png' in str(row['imagen']).lower():
            df.at[i, 'imagen'] = f"p{contador_img}.png"
            
        # Actualizar opciones si son imágenes
        for col, letra in zip(['opcion_a', 'opcion_b', 'opcion_c', 'opcion_d'], ['a', 'b', 'c', 'd']):
            if pd.notna(row[col]) and '.png' in str(row[col]).lower():
                df.at[i, col] = f"{letra}{contador_img}.png"
                
        contador_img += 1

# Guardar el CSV corregido con todas las comillas obligatorias
df.to_csv('fisica_ingenieria_corregido.csv', index=False, quoting=1)
print(f"¡Archivo de Física corregido! Guardado como 'fisica_ingenieria_corregido.csv'.")