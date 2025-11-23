"""
Configuración centralizada para el proyecto Indicadores de Comportamiento

Este archivo centraliza todas las rutas y configuraciones del proyecto.
Importa este archivo en tus notebooks en lugar de usar rutas hardcodeadas.

Uso en notebooks:
    from pathlib import Path
    import sys
    
    # Agregar la raíz del proyecto al path
    ROOT = Path().resolve().parent
    sys.path.insert(0, str(ROOT))
    
    from config import PATHS, CONFIG
"""

from pathlib import Path
import os

# ============================================================
# RUTAS DEL PROYECTO
# ============================================================

# Detectar automáticamente la raíz del proyecto
# Busca el directorio que contiene este archivo config.py
PROJECT_ROOT = Path(__file__).resolve().parent

class PATHS:
    """Rutas principales del proyecto"""
    
    # Raíz del proyecto
    ROOT = PROJECT_ROOT
    
    # Carpetas principales
    DATA = ROOT / "data"
    SRC = ROOT / "src"
    DOCS = ROOT / "docs"
    
    # Carpetas de datos
    RAW = DATA / "raw"
    RAW_FB = RAW / "FB"
    RAW_WA = RAW / "WA"
    
    PROCESSED = DATA / "processed"
    UNCLEANED = PROCESSED / "uncleaned"
    
    FEATURES = DATA / "features"
    FEATURES_FINAL = FEATURES / "final"
    
    RESULTS = DATA / "results"
    
    # Archivos principales
    PUBLICACIONES_CONSOLIDADO = PROCESSED / "publicaciones_consolidado.csv"
    PUBLICACIONES_COMPLETAS = PROCESSED / "publicaciones_completas.csv"
    PUBLICACIONES_TEXTO = PROCESSED / "publicaciones_texto.csv"
    
    CARACTERISTICAS_COMPLETAS = FEATURES / "caracteristicas_completas.csv"
    DATOS_PSICOMETRICOS = FEATURES / "datos_psicometricos.csv"
    DATASET_CONSOLIDADO = FEATURES_FINAL / "dataset_consolidado.csv"
    REQUERIMIENTOS = ROOT / "requirements.txt"
    
    @classmethod
    def crear_directorios(cls):
        """Crea todas las carpetas necesarias si no existen"""
        carpetas = [
            cls.DATA,
            cls.RAW, cls.RAW_FB, cls.RAW_WA,
            cls.PROCESSED, cls.UNCLEANED,
            cls.FEATURES, cls.FEATURES_FINAL,
            cls.RESULTS,
            cls.DOCS,
        ]
        
        for carpeta in carpetas:
            carpeta.mkdir(parents=True, exist_ok=True)
        
        print("✓ Estructura de carpetas verificada/creada")
        return True


# ============================================================
# CONFIGURACIÓN DE PROCESAMIENTO
# ============================================================

class CONFIG:
    """Configuraciones generales del proyecto"""
    
    # Configuración de participantes
    PREFIJO_ID = "EST"
    NUMERO_INICIAL = 1
    
    # Filtros de fecha
    USAR_FILTRO_FECHA = True
    MESES_ATRAS = 6
    FECHA_DESDE = None  # "2025-01-01" o None
    
    # Configuración de limpieza de texto
    MANTENER_HASHTAGS = False
    MANTENER_MENCIONES = False
    MANTENER_URLS = False
    LONGITUD_MINIMA_TEXTO = 10
    PALABRAS_MINIMAS = 3
    
    # Configuración de análisis
    USAR_PYSENTIMIENTO = True
    USAR_EMOJIS = True
    MOSTRAR_PROGRESO = True
    PROGRESO_CADA = 100
    
    # Encoding
    ENCODING = 'utf-8-sig'
    
    # Visualización
    FIGSIZE_DEFAULT = (14, 10)
    DPI = 300
    
    @classmethod
    def resumen(cls):
        """Muestra un resumen de la configuración actual"""
        print("=" * 60)
        print("CONFIGURACIÓN ACTUAL")
        print("=" * 60)
        print(f"Prefijo IDs: {cls.PREFIJO_ID}")
        print(f"Filtro de fecha: {'Activo' if cls.USAR_FILTRO_FECHA else 'Inactivo'}")
        if cls.USAR_FILTRO_FECHA:
            if cls.FECHA_DESDE:
                print(f"  Desde: {cls.FECHA_DESDE}")
            else:
                print(f"  Últimos {cls.MESES_ATRAS} meses")
        print(f"Análisis de sentimiento: {'Activo' if cls.USAR_PYSENTIMIENTO else 'Inactivo'}")
        print(f"Longitud mínima texto: {cls.LONGITUD_MINIMA_TEXTO} caracteres")
        print(f"Palabras mínimas: {cls.PALABRAS_MINIMAS}")
        print("=" * 60)


# ============================================================
# INICIALIZACIÓN
# ============================================================

# Crear carpetas automáticamente al importar
if not PATHS.DATA.exists():
    print("⚠️  Estructura de carpetas no encontrada. Creando...")
    PATHS.crear_directorios()


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def get_participant_file(participant_id: str, folder: Path = None) -> Path:
    """
    Obtiene la ruta del archivo de un participante
    
    Args:
        participant_id: ID del participante (ej: "EST001")
        folder: Carpeta donde buscar (por defecto: UNCLEANED)
    
    Returns:
        Path al archivo CSV del participante
    """
    if folder is None:
        folder = PATHS.UNCLEANED
    
    return folder / f"{participant_id}.csv"


def verificar_instalacion():
    """Verifica que todas las dependencias estén instaladas"""
    dependencias = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'beautifulsoup4': 'bs4',
        'openpyxl': 'openpyxl',
        'pysentimiento': 'pysentimiento',
        'emoji': 'emoji',
        'scipy': 'scipy',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
    }
    
    faltantes = []
    
    for nombre, modulo in dependencias.items():
        try:
            __import__(modulo)
        except ImportError:
            faltantes.append(nombre)
    
    if faltantes:
        print("⚠️  Dependencias faltantes:")
        for dep in faltantes:
            print(f"   - {dep}")
        print("\nInstala con: pip install -r requirements.txt")
        return False
    else:
        print("✓ Todas las dependencias instaladas correctamente")
        return True


if __name__ == "__main__":
    # Mostrar configuración cuando se ejecuta directamente
    print(f"\n📂 Raíz del proyecto: {PATHS.ROOT}\n")
    CONFIG.resumen()
    print("\n")
    verificar_instalacion()
    print("\n")
    PATHS.crear_directorios()
