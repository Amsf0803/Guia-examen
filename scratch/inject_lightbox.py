import os

TEMPLATES_DIR = 'templates'
FILES = [
    'resultados.html',
    'examen.html',
    'pregunta_detalle.html',
    'pregunta_lectura_detalle.html',
    'flashcards.html',
    'flashcards_lectura.html'
]

css_link = """    <link rel="stylesheet" href="{{ url_for('static', filename='css/lightbox.css') }}">
</head>"""

js_link = """    <script src="{{ url_for('static', filename='js/lightbox.js') }}"></script>
</body>"""

for filename in FILES:
    filepath = os.path.join(TEMPLATES_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        
        if 'lightbox.js' not in content:
            content = content.replace('</head>', css_link)
            content = content.replace('</body>', js_link)
            
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"Injected into {filename}")
        else:
            print(f"Skipped {filename} (already injected)")
    else:
        print(f"File not found: {filename}")
