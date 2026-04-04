temario_estudio = {
    "Superior": {
        "Matemáticas": [
            {
                "id": "mat_1_1_1",
                "titulo": "1.1.1 Sucesiones numéricas",
                "explicacion": r"""
                <p>Una <strong>sucesión numérica</strong> es un conjunto ordenado de números que siguen una regla o patrón específico. Cada número en la sucesión se llama <em>término</em>.</p>
                <ul>
                    <li><strong>Progresión Aritmética:</strong> La diferencia entre términos consecutivos es constante. Se suma o resta siempre la misma cantidad. Fórmula del término general: $$a_n = a_1 + (n - 1)d$$ donde $a_1$ es el primer término y $d$ es la diferencia.</li>
                    <li><strong>Progresión Geométrica:</strong> La razón entre términos consecutivos es constante. Se multiplica o divide siempre por la misma cantidad. Fórmula: $$a_n = a_1 \cdot r^{n - 1}$$ donde $r$ es la razón.</li>
                </ul>
                """,
                "ejercicios": [
                    {
                        "pregunta": r"¿Cuál es el décimo término de la sucesión: $3, 7, 11, 15, \dots$?",
                        "solucion": r"""
                        <strong>Paso 1:</strong> Identificar el tipo de sucesión. Observamos que $7-3=4$, $11-7=4$. Es una progresión aritmética con diferencia $d = 4$.<br>
                        <strong>Paso 2:</strong> Identificar el primer término: $a_1 = 3$.<br>
                        <strong>Paso 3:</strong> Sustituir en la fórmula general para $n=10$:<br>
                        $$a_{10} = 3 + (10 - 1)(4)$$<br>
                        $$a_{10} = 3 + (9)(4)$$<br>
                        $$a_{10} = 3 + 36 = 39$$<br>
                        <strong>Respuesta:</strong> El décimo término es 39.
                        """
                    },
                    {
                        "pregunta": r"Encuentra el 6° término de la sucesión: $2, 6, 18, 54, \dots$",
                        "solucion": r"""
                        <strong>Paso 1:</strong> Identificar el patrón. Vemos que $6 \div 2 = 3$, $18 \div 6 = 3$. Es una progresión geométrica con razón $r = 3$.<br>
                        <strong>Paso 2:</strong> El primer término es $a_1 = 2$.<br>
                        <strong>Paso 3:</strong> Sustituir en la fórmula para $n=6$:<br>
                        $$a_6 = 2 \cdot (3)^{6 - 1}$$<br>
                        $$a_6 = 2 \cdot (3)^5$$<br>
                        $$a_6 = 2 \cdot 243 = 486$$<br>
                        <strong>Respuesta:</strong> El sexto término es 486.
                        """
                    }
                ]
            },
            {
                "id": "mat_1_1_2",
                "titulo": "1.1.2 Secuencias alfanuméricas",
                "explicacion": "<p>Tema en desarrollo. En esta sección se estudia cómo analizar secuencias que mezclan letras y números con diferentes patrones combinados.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_1_1_3",
                "titulo": "1.1.3 Expresiones generales",
                "explicacion": "<p>Tema en desarrollo. Contiene el estudio para hallar la regla matemática general o el $n$-ésimo término para cualquier secuencia dada.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_1_2_1",
                "titulo": "1.2.1 Secuencias con patrones geométricos",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_1_2_2",
                "titulo": "1.2.2 Operaciones de simetría",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_1_2_3",
                "titulo": "1.2.3 Perspectivas y cortes de figuras",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_1_3_1",
                "titulo": "1.3.1 Medida de figuras y objetos",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_1_4_1",
                "titulo": "1.4.1 Conjunto de datos y análisis de la información",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_1_5_1",
                "titulo": "1.5.1 Resolución de problemas",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_2_1_1",
                "titulo": "2.1.1 Propiedades (Números reales)",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_2_1_2",
                "titulo": "2.1.2 Operaciones básicas",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_2_1_3",
                "titulo": "2.1.3 Proporciones",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_2_2_1",
                "titulo": "2.2.1 Lenguaje algebraico",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_2_2_2",
                "titulo": "2.2.2 Expresiones fraccionarias",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_2_2_3",
                "titulo": "2.2.3 Leyes de los exponentes y radicales",
                "explicacion": "<p>Tema en desarrollo. $x^a \cdot x^b = x^{a+b}$ y otras propiedades de exponentes.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_2_2_4",
                "titulo": "2.2.4 Productos notables",
                "explicacion": r"""
                <p>Los <strong>productos notables</strong> son multiplicaciones de polinomios cuyos resultados pueden obtenerse directamente mediante reglas fijas, sin necesidad de hacer la multiplicación término a término.</p>
                <ul>
                    <li><strong>Binomio al cuadrado:</strong> El cuadrado del primer término, más el doble del primero por el segundo, más el cuadrado del segundo.<br> $$(a \pm b)^2 = a^2 \pm 2ab + b^2$$</li>
                    <li><strong>Binomios conjugados:</strong> El producto de la suma por la diferencia de dos cantidades es igual a una diferencia de cuadrados.<br> $$(a + b)(a - b) = a^2 - b^2$$</li>
                    <li><strong>Binomios con término común:</strong> El cuadrado del común, más la suma de los no comunes por el común, más el producto de los no comunes.<br> $$(x + a)(x + b) = x^2 + (a+b)x + ab$$</li>
                </ul>
                """,
                "ejercicios": [
                    {
                        "pregunta": r"Desarrolla el siguiente binomio al cuadrado: $(3x + 5y)^2$",
                        "solucion": r"""
                        <strong>Paso 1:</strong> Identificar la regla a usar: $(a + b)^2 = a^2 + 2ab + b^2$.<br>
                        <strong>Paso 2:</strong> Asignar valores: $a = 3x$ y $b = 5y$.<br>
                        <strong>Paso 3:</strong> Aplicar la regla:<br>
                        $$(3x)^2 + 2(3x)(5y) + (5y)^2$$<br>
                        <strong>Paso 4:</strong> Simplificar cada término:<br>
                        $$9x^2 + 30xy + 25y^2$$<br>
                        <strong>Respuesta:</strong> $9x^2 + 30xy + 25y^2$
                        """
                    },
                    {
                        "pregunta": r"Resuelve el producto de binomios conjugados: $(4m^2 - 7n)(4m^2 + 7n)$",
                        "solucion": r"""
                        <strong>Paso 1:</strong> Aplicar la regla de diferencia de cuadrados: $(a - b)(a + b) = a^2 - b^2$.<br>
                        <strong>Paso 2:</strong> Aquí $a = 4m^2$ y $b = 7n$.<br>
                        <strong>Paso 3:</strong> Elevar cada término al cuadrado:<br>
                        $$(4m^2)^2 - (7n)^2$$<br>
                        <strong>Paso 4:</strong> Simplificar (recordando multiplicar los exponentes):<br>
                        $$16m^4 - 49n^2$$<br>
                        <strong>Respuesta:</strong> $16m^4 - 49n^2$
                        """
                    }
                ]
            },
            {
                "id": "mat_2_2_5",
                "titulo": "2.2.5 Métodos de factorización",
                "explicacion": "<p>Tema en desarrollo. Factor común, agrupación, trinomios cuadrados perfectos y otros métodos.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_2_3_1",
                "titulo": "2.3.1 Concepto de función",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_2_3_2",
                "titulo": "2.3.2 Propiedades de las igualdades",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_2_3_3",
                "titulo": "2.3.3 Ecuaciones lineales",
                "explicacion": "<p>Tema en desarrollo. Resolución de $ax + b = 0$.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_2_3_4",
                "titulo": "2.3.4 Sistemas de ecuaciones lineales",
                "explicacion": "<p>Tema en desarrollo. Sustitución, igualación, reducción, Cramer.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_2_4_1",
                "titulo": "2.4.1 Concepto de función cuadrática",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_2_4_2",
                "titulo": "2.4.2 Ecuaciones cuadráticas",
                "explicacion": "<p>Tema en desarrollo. General: $\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$</p>",
                "ejercicios": []
            },
            {
                "id": "mat_3_1_1",
                "titulo": "3.1.1 Conceptos (Funciones exp y log)",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_3_1_2",
                "titulo": "3.1.2 Propiedades (Funciones exp y log)",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_3_2_1",
                "titulo": "3.2.1 Elementos básicos (Geometría)",
                "explicacion": "<p>Tema en desarrollo. Puntos, rectas, planos y axiomas de Euclides.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_3_2_2",
                "titulo": "3.2.2 Triángulos",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_3_2_3",
                "titulo": "3.2.3 Polígonos",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_3_2_4",
                "titulo": "3.2.4 Circunferencia (Geometría Euclidiana)",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_3_3_1",
                "titulo": "3.3.1 Representación gráfica (Funciones trigonométricas)",
                "explicacion": "<p>Tema en desarrollo. Gráficas de Seno, Coseno, Tangente.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_3_3_2",
                "titulo": "3.3.2 Identidades trigonométricas",
                "explicacion": "<p>Tema en desarrollo. Relaciones Pitagóricas, recíprocas y por cociente.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_3_3_3",
                "titulo": "3.3.3 Razones trigonométricas",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_4_1_1",
                "titulo": "4.1.1 Plano cartesiano",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_4_1_2",
                "titulo": "4.1.2 Línea recta",
                "explicacion": "<p>Tema en desarrollo. Pendiente, ecuación punto-pendiente $y-y_1=m(x-x_1)$.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_4_2_1",
                "titulo": "4.2.1 Circunferencia (Geometría Analítica)",
                "explicacion": "<p>Tema en desarrollo. Ecuación general y ordinaria de la circunferencia.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_4_2_2",
                "titulo": "4.2.2 Parábola",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_4_2_3",
                "titulo": "4.2.3 Elipse",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_4_2_4",
                "titulo": "4.2.4 Hipérbola",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_4_3_1",
                "titulo": "4.3.1 Plano polar",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_5_1_1",
                "titulo": "5.1.1 Dominio y rango",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_5_1_2",
                "titulo": "5.1.2 Desigualdades",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_5_1_3",
                "titulo": "5.1.3 Definición de límite",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_5_1_4",
                "titulo": "5.1.4 Teoremas de límites",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_5_1_5",
                "titulo": "5.1.5 Límites al infinito",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_5_1_6",
                "titulo": "5.1.6 Continuidad de una función",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_5_2_1",
                "titulo": "5.2.1 Definición de derivada",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_5_2_2",
                "titulo": "5.2.2 Interpretación geométrica",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_5_2_3",
                "titulo": "5.2.3 Fórmulas de derivadas",
                "explicacion": "<p>Tema en desarrollo. Derivadas básicas: polonimos, exponenciales y trigonométricas.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_5_2_4",
                "titulo": "5.2.4 Regla de la cadena",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_5_2_5",
                "titulo": "5.2.5 Máximos y mínimos",
                "explicacion": "<p>Tema en desarrollo. Criterio de la primera y segunda derivada.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_6_1_1",
                "titulo": "6.1.1 Definición de la antiderivada",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_6_1_2",
                "titulo": "6.1.2 Constante de integración",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_6_1_3",
                "titulo": "6.1.3 Fórmulas básicas de integración",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_6_2_1",
                "titulo": "6.2.1 Por sustitución",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_6_2_2",
                "titulo": "6.2.2 Integración por partes",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_6_2_3",
                "titulo": "6.2.3 Sustitución trigonométrica",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_6_2_4",
                "titulo": "6.2.4 Fracciones parciales",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_6_3_1",
                "titulo": "6.3.1 Teorema fundamental del cálculo",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_6_3_2",
                "titulo": "6.3.2 Área bajo la curva",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_6_3_3",
                "titulo": "6.3.3 Longitud de arco",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_7_1_1",
                "titulo": "7.1.1 Teoría de conjuntos",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_7_1_2",
                "titulo": "7.1.2 Técnicas de conteo",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_7_1_3",
                "titulo": "7.1.3 Espacios muestrales",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_7_1_4",
                "titulo": "7.1.4 Probabilidad de un evento",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_7_1_5",
                "titulo": "7.1.5 Eventos aleatorios",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_7_1_6",
                "titulo": "7.1.6 Probabilidad condicional",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_7_1_7",
                "titulo": "7.1.7 Eventos dependientes e independientes",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_7_1_8",
                "titulo": "7.1.8 Teorema de Bayes",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_7_2_1",
                "titulo": "7.2.1 Tablas de distribución de frecuencias",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_7_2_2",
                "titulo": "7.2.2 Gráficas de datos",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_7_2_3",
                "titulo": "7.2.3 Muestra y población",
                "explicacion": "<p>Tema en desarrollo.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_7_2_4",
                "titulo": "7.2.4 Medidas de tendencia central",
                "explicacion": "<p>Tema en desarrollo. Media, mediana y moda.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_7_2_5",
                "titulo": "7.2.5 Medidas de posicion",
                "explicacion": "<p>Tema en desarrollo. Cuartiles, deciles y percentiles.</p>",
                "ejercicios": []
            },
            {
                "id": "mat_7_2_6",
                "titulo": "7.2.6 Medidas de dispersion",
                "explicacion": "<p>Tema en desarrollo. Varianza y desviación estándar.</p>",
                "ejercicios": []
            }
        ]
    },
    "Medio Superior": {
        "Matemáticas": [
            {
                "id": "mat_nms_1",
                "titulo": "1.1 Jerarquía de Operaciones (Secundaria)",
                "explicacion": r"""
                <p>La <strong>jerarquía de operaciones</strong> es el orden correcto en el que deben resolverse las operaciones en una expresión matemática.</p>
                <ol>
                    <li>Paréntesis, corchetes y llaves $()$, $[]$, $\{\}$.</li>
                    <li>Potencias y raíces $x^2$, $\sqrt{x}$.</li>
                    <li>Multiplicaciones y divisiones $\times$, $\div$ (de izquierda a derecha).</li>
                    <li>Sumas y restas $+$, $-$ (de izquierda a derecha).</li>
                </ol>
                """,
                "ejercicios": [
                    {
                        "pregunta": r"Resuelve: $5 + 3 \times (8 - 2)^2 \div 4$",
                        "solucion": r"""
                        <strong>Paso 1 (Paréntesis):</strong> $8 - 2 = 6$<br>
                        La expresión queda: $5 + 3 \times (6)^2 \div 4$<br>
                        <strong>Paso 2 (Potencias):</strong> $6^2 = 36$<br>
                        La expresión queda: $5 + 3 \times 36 \div 4$<br>
                        <strong>Paso 3 (Multiplicación y División de izq a der):</strong> $3 \times 36 = 108$, luego $108 \div 4 = 27$<br>
                        La expresión queda: $5 + 27$<br>
                        <strong>Paso 4 (Suma):</strong> $5 + 27 = 32$<br>
                        <strong>Respuesta:</strong> $32$
                        """
                    }
                ]
            }
        ]
    }
}
