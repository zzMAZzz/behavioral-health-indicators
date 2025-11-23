# Indicadores de Comportamiento y Salud Mental mediante Wearables

## Descripción

Este repositorio contiene la implementación completa de un proyecto de investigación que analiza la relación entre **indicadores digitales de comportamiento** (extraídos de redes sociales como Facebook y WhatsApp) y **medidas psicométricas de salud mental** (depresión, ansiedad, estrés y soledad).

El proyecto utiliza técnicas avanzadas de **Procesamiento de Lenguaje Natural (NLP)** con modelos transformers en español ([pysentimiento](https://github.com/pysentimiento/pysentimiento)) para extraer 41 características emocionales y lingüísticas de publicaciones digitales, y las correlaciona con escalas clínicas validadas (DASS-21, UCLA Loneliness Scale).

##  Objetivo

- **Identificar** patrones lingüísticos y emocionales en redes sociales asociados con indicadores de salud mental
- **Validar** el uso de indicadores digitales como herramienta complementaria a evaluaciones psicométricas tradicionales
- **Desarrollar** una metodología replicable y científicamente rigurosa para el análisis de comportamiento digital
- **Contribuir** al campo emergente de la psicología digital y salud mental preventiva

##  Estado del Proyecto

-  **Participantes**: 22 estudiantes universitarios
-  **Publicaciones analizadas**: +6,600 textos de redes sociales
-  **Características extraídas**: 41 por publicación
-  **Fase actual**: Análisis estadístico y modelado predictivo

## 🛠️ Tecnologías y Herramientas

### Lenguaje Base
- **Python 3.8+**: Lenguaje principal del proyecto

### Procesamiento de Lenguaje Natural
- **[pysentimiento](https://github.com/pysentimiento/pysentimiento)**: Análisis de sentimiento y emociones (modelos transformer en español)
- **spaCy**: Procesamiento avanzado de texto
- **emoji**: Análisis de emojis

### Análisis de Datos
- **pandas**: Manipulación y análisis de datos tabulares
- **numpy**: Computación numérica
- **scipy**: Análisis estadístico (correlaciones, tests, bootstrap)

### Visualización
- **matplotlib**: Gráficos estáticos
- **seaborn**: Visualizaciones estadísticas avanzadas

### Extracción de Datos
- **BeautifulSoup**: Parsing de HTML (Facebook)
- **regex**: Extracción de texto estructurado (WhatsApp)

### Machine Learning (Opcional)
- **scikit-learn**: Modelos predictivos y validación cruzada

## 📁 Estructura del Proyecto

```
Indicadores_Comportamiento/
├── config.py                    # Configuración centralizada
├── requirements.txt             # Dependencias
├── README.md                    # Este archivo
│
├── data/                        # Datos del proyecto
│   ├── raw/                     # Datos crudos originales
│   │   ├── FB/                  # Exportaciones de Facebook
│   │   └── WA/                  # Exportaciones de WhatsApp
│   ├── processed/               # Datos procesados
│   │   ├── uncleaned/           # CSVs individuales por participante
│   │   └── *.csv                # Datos consolidados y limpios
│   ├── features/                # Características extraídas
│   │   ├── final/               # Dataset consolidado final
│   │   └── *.csv                # Características y datos psicométricos
│   └── results/                 # Resultados de análisis
│
├── src/                         # Notebooks de análisis
│   ├── 1 - DataExtraction_FB.ipynb          # Extracción de Facebook
│   ├── 2 - DataExtraction_WA.ipynb          # Extracción de WhatsApp
│   ├── 3 - DataExtraction_Psicometricos.ipynb
│   ├── 4 - Preprocessing.ipynb              # Limpieza de datos
│   ├── 5 - EmotionalAnalysis.ipynb          # Análisis de sentimiento
│   ├── 6 - Correlaciones.ipynb              # Análisis de correlaciones
│
└── scripts/                     # Scripts de utilidad
    └── validacion_sentimiento.py            # Validación del modelo

```

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/zzMAZzz/behavioral-health-indicators
cd Indicadores_Comportamiento
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Verificar e instalar dependencias

```bash
pip install -r requirements.txt
python config.py
```

## 📖 Uso

### Pipeline Completo

Ejecuta los notebooks en orden numérico para replicar el análisis completo:

#### Fase 1: Extracción de Datos
1. **`1 - DataExtraction_FB.ipynb`**: Extracción de publicaciones de Facebook (HTML)
2. **`2 - DataExtraction_WA.ipynb`**: Extracción de chats de WhatsApp (archivos .txt)
3. **`3 - DataExtraction_Psicometricos.ipynb`**: Recopilación de datos psicométricos (DASS-21, UCLA)

#### Fase 2: Preprocesamiento
4. **`4 - Preprocessing.ipynb`**: Limpieza, normalización y consolidación de textos
5. **`4.5 - Caracteristicas_Temporales.ipynb`**: Extracción de características temporales

#### Fase 3: Análisis
6. **`5 - EmotionalAnalysis.ipynb`**: Análisis de sentimiento y extracción de 41 características
7. **`6 - Correlaciones.ipynb`**: Análisis de correlaciones entre indicadores digitales y psicométricos
8. **`7 - Bootstrap_IC.ipynb`**: Intervalos de confianza y validación estadística

#### Fase 4: Modelado (Opcional)
9. **`8 - Modelos_Predictivos.ipynb`**: Modelos de clasificación y predicción
10. **`9 - Clustering.ipynb`**: Agrupamiento de perfiles de comportamiento
11. **`10 - Perfiles_Individuales.ipynb`**: Análisis por participante


### Uso de Configuración Centralizada

```python
# En tus notebooks
from pathlib import Path
import sys

ROOT = Path().resolve().parent
sys.path.insert(0, str(ROOT))

from config import PATHS, CONFIG

# Usar rutas centralizadas
df = pd.read_csv(PATHS.PUBLICACIONES_TEXTO)

# Guardar resultados
df.to_csv(PATHS.RESULTS / "mi_analisis.csv", index=False)
```

Ver `src/EJEMPLO_USO_CONFIG.ipynb` para más ejemplos.

### Validación del Modelo de Sentimiento

```bash
# 1. Crear muestra para validación manual
python scripts/validacion_sentimiento.py --muestra 100

# 2. Etiquetar manualmente el archivo generado

# 3. Evaluar precisión
python scripts/validacion_sentimiento.py --evaluar
```

##  Características Extraídas

### Indicadores Lingüísticos (9)
- Número de palabras, caracteres
- Riqueza léxica
- Signos de puntuación
- etc.

### Indicadores de Pronombres (8)
- Uso de 1era persona singular/plural
- Uso de 2da/3era persona

### Palabras Psicológicas (8)
- Absolutistas (siempre, nunca)
- Negativas (no, ni, sin)
- Causales (porque, debido)
- Tentativas (quizás, tal vez)

### Sentimiento y Emoción (13)
- Sentimiento: Positivo, Negativo, Neutral
- Emociones: Alegría, Tristeza, Enojo, Miedo, Sorpresa, Disgusto

### Emojis (2)
- Cantidad total
- Emojis por palabra

**Total: 41 características** + metadatos

## 📈 Medidas Psicométricas

- **UCLA Loneliness Scale**: Soledad
- **DASS-21**: Depresión, Ansiedad, Estrés
- Variables demográficas

## 🔬 Validación de Resultados

El proyecto incluye múltiples niveles de validación:

-  Validación del modelo de sentimiento
-  Corrección por comparaciones múltiples (Bonferroni/FDR)
-  Intervalos de confianza bootstrap
-  Validación cruzada (pendiente con n=20)

## ⚠️ Consideraciones Éticas y Limitaciones

### Privacidad y Confidencialidad
-  **Anonimización**: Todos los datos personales han sido anonimizados
-  **Consentimiento informado**: Todos los participantes firmaron consentimiento
-  **Cumplimiento ético**: Proyecto aprobado por comité de ética (si aplica)
-  **Datos no incluidos**: Por razones de privacidad, los datos crudos no están en el repositorio

### Limitaciones del Estudio
- **Muestra**: n=22 estudiantes universitarios (limitación en generalización)
- **Diseño**: Correlacional (no permite inferencia causal)
- **Plataformas**: Solo Facebook y WhatsApp (no incluye otras redes)
- **Idioma**: Análisis optimizado para español
- **Temporalidad**: Análisis transversal (no longitudinal)

## 📝 Resultados Principales

### Correlaciones Significativas (Spearman, n=18)

Los análisis revelaron correlaciones significativas entre indicadores digitales y medidas psicométricas, destacando:

#### Soledad (UCLA Loneliness Scale)
| Indicador Digital | ρ (rho) | Interpretación |
|-------------------|---------|----------------|
| Sentimiento Positivo | r > 0.80 | Correlación muy alta |
| Ratio Pos/Neg | r > 0.80 | Correlación muy alta |
| Uso de Emojis | r ~ 0.70 | Correlación alta |
| Sentimiento Negativo | r ~ -0.70 | Correlación inversa alta |

#### Depresión, Ansiedad y Estrés (DASS-21)
- Correlaciones moderadas con indicadores lingüísticos
- Patrones de uso de pronombres personales
- Frecuencia de palabras absolutistas y negativas

### Validación Estadística
-  **Corrección por comparaciones múltiples**: FDR (Benjamini-Hochberg)
-  **Intervalos de confianza**: Bootstrap (10,000 iteraciones)
-  **Validación del modelo NLP**: Precisión > 85% en sentimiento

**Nota**: Todos los resultados han sido validados estadísticamente. Ver `data/results/` para análisis detallados.

## 🤝 Contribuciones

Este es un proyecto de investigación académica. Para contribuir:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto bajo licencia MIT.

## 👤 Autor

Miguel Zelaya  
Proyecto de Investigación en Indicadores de Comportamiento Digital

## 📚 Referencias

### Herramientas y Bibliotecas
- **pysentimiento**: Pérez, J. M., et al. (2021). [pysentimiento: A Python Toolkit for Sentiment Analysis and Social NLP tasks](https://github.com/pysentimiento/pysentimiento)

### Escalas Psicométricas
- **DASS-21**: Lovibond, P. F., & Lovibond, S. H. (1995). *The structure of negative emotional states: Comparison of the Depression Anxiety Stress Scales (DASS) with the Beck Depression and Anxiety Inventories*. Behaviour Research and Therapy, 33(3), 335-343.
- **UCLA Loneliness Scale**: Russell, D. W. (1996). *UCLA Loneliness Scale (Version 3): Reliability, validity, and factor structure*. Journal of Personality Assessment, 66(1), 20-40.

## 📊 Citación

Si utilizas este código o metodología en tu investigación, por favor cita:

```bibtex
@misc{zelaya2025indicadores,
  author = {Zelaya, Miguel},
  title = {Indicadores de Comportamiento Digital y Salud Mental},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/zzMAZzz/behavioral-health-indicators}
}
```

---

**Última actualización**: Noviembre 2025  
**Versión**: 1.0  
**Estado**: En desarrollo activo

Para más información, consulta la documentación o abre un **Issue** en GitHub.

## 🔮 Trabajo Futuro
- [ ] **Expandir muestra**: Incrementar a n > 50 para mayor poder estadístico
- [ ] **Análisis longitudinal**: Estudiar evolución temporal de indicadores
- [ ] **Más plataformas**: Incluir Instagram, Twitter, TikTok
- [ ] **Modelos predictivos**: Desarrollar modelos de clasificación robustos
- [ ] **Dashboard interactivo**: Herramienta de visualización en tiempo real
- [ ] **Validación cruzada**: Con poblaciones diferentes
- [ ] **Publicación académica**: Preparar manuscript para revista científica

## 🤝 Cómo Contribuir

Este proyecto está abierto a colaboraciones académicas:

1. **Fork** el repositorio
2. Crea una **rama** para tu contribución (`git checkout -b feature/mejora`)
3. **Commit** tus cambios con mensajes descriptivos
4. **Push** a tu rama (`git push origin feature/mejora`)
5. Abre un **Pull Request** con descripción detallada

### Áreas de Colaboración
- Mejoras en el pipeline de NLP
- Nuevas características psicológicas
- Validación en otras poblaciones
- Optimización de modelos
- Documentación y ejemplos

## 📄 Licencia

Este proyecto se publica bajo la licencia **MIT**. Ver archivo `LICENSE` para más detalles.

Los datos personales están protegidos y no se incluyen en el repositorio por razones de privacidad y ética.

## 📧 Contacto

**Miguel Zelaya**  
📧 Email: [mzelayaf@unah.hn]  
🔗 GitHub: [@zzMAZzz](https://github.com/zzMAZzz)  
💼 LinkedIn: [Miguel Zelaya](https://github.com/zzMAZzz) 

Para preguntas sobre el proyecto, metodología o colaboraciones, no dudes en abrir un **Issue** o contactarme directamente.

## 🙏 Agradecimientos

- A todos los **participantes** que compartieron sus datos voluntariamente
- Al equipo de [**pysentimiento**](https://github.com/pysentimiento/pysentimiento) por su excelente biblioteca
