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
                "id": "mat_2_2_4",
                "titulo": "2.2.4 Productos Notables",
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
