"""
Script para Validación Manual del Modelo de Sentimiento

Este script:
1. Selecciona una muestra aleatoria de publicaciones
2. Exporta un CSV para etiquetado manual
3. Compara las etiquetas manuales con las automáticas
4. Genera reporte de precisión

Uso:
    python scripts/validacion_sentimiento.py --muestra 100
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import argparse

# Agregar raíz al path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config import PATHS, CONFIG
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt


def crear_muestra_validacion(n_muestra=100, seed=42):
    """
    Crea archivo CSV con muestra aleatoria para validación manual
    
    Args:
        n_muestra: Número de publicaciones a muestrear
        seed: Semilla para reproducibilidad
    
    Returns:
        DataFrame con la muestra
    """
    print("="*80)
    print("CREACIÓN DE MUESTRA PARA VALIDACIÓN MANUAL")
    print("="*80)
    
    # Cargar datos
    df_caract = pd.read_csv(PATHS.CARACTERISTICAS_COMPLETAS, encoding=CONFIG.ENCODING)
    df_texto = pd.read_csv(PATHS.PUBLICACIONES_TEXTO, encoding=CONFIG.ENCODING)
    
    # Merge para tener texto y sentimiento
    df = df_caract.merge(
        df_texto[['id_publicacion', 'texto_publicacion']], 
        on='id_publicacion'
    )
    
    print(f"✓ Total de publicaciones: {len(df)}")
    
    # Muestreo estratificado por sentimiento
    muestra = df.groupby('sentimiento', group_keys=False).apply(
        lambda x: x.sample(min(len(x), n_muestra//3), random_state=seed)
    )
    
    # Si no llegamos a n_muestra, completar aleatoriamente
    if len(muestra) < n_muestra:
        restantes = df[~df['id_publicacion'].isin(muestra['id_publicacion'])]
        extra = restantes.sample(
            min(n_muestra - len(muestra), len(restantes)), 
            random_state=seed
        )
        muestra = pd.concat([muestra, extra])
    
    # Seleccionar solo columnas necesarias
    muestra_export = muestra[[
        'id_publicacion',
        'id_participante', 
        'texto_publicacion',
        'sentimiento'
    ]].copy()
    
    # Agregar columna para etiquetado manual (vacía)
    muestra_export['sentimiento_manual'] = ''
    
    # Reordenar columnas
    muestra_export = muestra_export[[
        'id_publicacion',
        'id_participante',
        'texto_publicacion',
        'sentimiento',
        'sentimiento_manual'
    ]]
    
    # Guardar
    archivo_salida = PATHS.RESULTS / 'muestra_validacion_manual.csv'
    muestra_export.to_csv(archivo_salida, index=False, encoding=CONFIG.ENCODING)
    
    print(f"\n✓ Muestra creada: {len(muestra_export)} publicaciones")
    print(f"✓ Guardado en: {archivo_salida}")
    
    print("\nDistribución de sentimientos en la muestra:")
    print(muestra_export['sentimiento'].value_counts())
    
    print("\n" + "="*80)
    print("INSTRUCCIONES PARA ETIQUETADO MANUAL:")
    print("="*80)
    print("1. Abre el archivo: muestra_validacion_manual.csv")
    print("2. Lee cada 'texto_publicacion'")
    print("3. En 'sentimiento_manual', escribe:")
    print("   - POS (positivo)")
    print("   - NEG (negativo)")
    print("   - NEU (neutral)")
    print("4. Guarda el archivo como: muestra_validacion_manual_etiquetada.csv")
    print("5. Ejecuta: python scripts/validacion_sentimiento.py --evaluar")
    print("="*80)
    
    return muestra_export


def evaluar_precision():
    """
    Evalúa la precisión del modelo comparando con etiquetas manuales
    """
    print("="*80)
    print("EVALUACIÓN DE PRECISIÓN DEL MODELO")
    print("="*80)
    
    # Cargar archivo etiquetado manualmente
    archivo_manual = PATHS.RESULTS / 'muestra_validacion_manual_etiquetada.csv'
    
    if not archivo_manual.exists():
        print(f"\nError: No se encuentra {archivo_manual}")
        print("   Primero etiqueta manualmente el archivo")
        return
    
    df_manual = pd.read_csv(archivo_manual, encoding=CONFIG.ENCODING)
    
    # Validar que se completó el etiquetado
    if df_manual['sentimiento_manual'].isna().any() or (df_manual['sentimiento_manual'] == '').any():
        print("\nAdvertencia: Hay publicaciones sin etiquetar")
        print(f"   Sin etiquetar: {df_manual['sentimiento_manual'].isna().sum() + (df_manual['sentimiento_manual'] == '').sum()}")
    
    # Filtrar solo las etiquetadas
    df_validacion = df_manual[
        (df_manual['sentimiento_manual'].notna()) & 
        (df_manual['sentimiento_manual'] != '')
    ].copy()
    
    print(f"\n✓ Publicaciones validadas: {len(df_validacion)}")
    
    # Normalizar etiquetas (mayúsculas, limpiar espacios)
    df_validacion['sentimiento_manual'] = df_validacion['sentimiento_manual'].str.strip().str.upper()
    df_validacion['sentimiento'] = df_validacion['sentimiento'].str.strip().str.upper()
    
    # Métricas
    y_true = df_validacion['sentimiento_manual']
    y_pred = df_validacion['sentimiento']
    
    accuracy = accuracy_score(y_true, y_pred)
    
    print("\n" + "="*80)
    print(f"ACCURACY: {accuracy:.2%}")
    print("="*80)
    
    # Reporte detallado
    print("\nREPORTE DE CLASIFICACIÓN:")
    print("-"*80)
    report = classification_report(y_true, y_pred)
    print(report)
    
    # Matriz de confusión
    print("\nMATRIZ DE CONFUSIÓN:")
    print("-"*80)
    cm = confusion_matrix(y_true, y_pred, labels=['POS', 'NEU', 'NEG'])
    cm_df = pd.DataFrame(
        cm,
        index=['POS (real)', 'NEU (real)', 'NEG (real)'],
        columns=['POS (pred)', 'NEU (pred)', 'NEG (pred)']
    )
    print(cm_df)
    
    # Visualizar matriz de confusión
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm_df, annot=True, fmt='d', cmap='Blues', cbar=True)
    plt.title(f'Matriz de Confusión - Accuracy: {accuracy:.2%}')
    plt.ylabel('Sentimiento Real')
    plt.xlabel('Sentimiento Predicho')
    plt.tight_layout()

    # Cambiar .png por .pdf
    archivo_viz = PATHS.RESULTS / 'confusion_matrix_sentimiento.pdf'
    plt.savefig(archivo_viz, dpi=300, bbox_inches='tight')
    print(f"\n✓ Matriz guardada en: {archivo_viz}")
    plt.show()
    
    # Análisis de errores
    errores = df_validacion[df_validacion['sentimiento'] != df_validacion['sentimiento_manual']]
    
    if len(errores) > 0:
        print("\n" + "="*80)
        print(f"ANÁLISIS DE ERRORES ({len(errores)} casos):")
        print("="*80)
        
        archivo_errores = PATHS.RESULTS / 'errores_sentimiento.csv'
        errores[['id_publicacion', 'texto_publicacion', 'sentimiento', 'sentimiento_manual']].to_csv(
            archivo_errores, 
            index=False, 
            encoding=CONFIG.ENCODING
        )
        print(f"✓ Errores exportados a: {archivo_errores}")
        
        # Mostrar algunos ejemplos
        print("\nEjemplos de errores:")
        print("-"*80)
        for idx, row in errores.head(5).iterrows():
            print(f"\nTexto: {row['texto_publicacion'][:100]}...")
            print(f"Predicho: {row['sentimiento']} | Real: {row['sentimiento_manual']}")
    
    # Guardar reporte
    archivo_reporte = PATHS.RESULTS / 'validacion_sentimiento_reporte.txt'
    with open(archivo_reporte, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("REPORTE DE VALIDACIÓN DE SENTIMIENTO\n")
        f.write("="*80 + "\n\n")
        f.write(f"Publicaciones validadas: {len(df_validacion)}\n")
        f.write(f"Accuracy: {accuracy:.2%}\n\n")
        f.write("REPORTE DE CLASIFICACIÓN:\n")
        f.write("-"*80 + "\n")
        f.write(report)
        f.write("\n\nMATRIZ DE CONFUSIÓN:\n")
        f.write("-"*80 + "\n")
        f.write(str(cm_df))
        f.write("\n\n" + "="*80 + "\n")
        
        if accuracy >= 0.75:
            f.write("✓ RESULTADO: ACEPTABLE (≥75%)\n")
        elif accuracy >= 0.60:
            f.write("⚠️ RESULTADO: MARGINAL (60-75%)\n")
        else:
            f.write("❌ RESULTADO: BAJO (<60%)\n")
        
        f.write("="*80 + "\n")
    
    print(f"\n✓ Reporte completo guardado en: {archivo_reporte}")
    
    # Interpretación
    print("\n" + "="*80)
    print("INTERPRETACIÓN:")
    print("="*80)
    if accuracy >= 0.75:
        print("✓ El modelo tiene una precisión ACEPTABLE")
        print("  Los resultados del análisis de sentimiento son confiables")
    elif accuracy >= 0.60:
        print("⚠️ El modelo tiene una precisión MARGINAL")
        print("  Los resultados deben interpretarse con cautela")
        print("  Considera usar un modelo diferente o afinar parámetros")
    else:
        print("❌ El modelo tiene una precisión BAJA")
        print("  Los resultados NO son confiables")
        print("  Se recomienda cambiar de modelo o revisar los datos")
    print("="*80)


def main():
    parser = argparse.ArgumentParser(description='Validación del modelo de sentimiento')
    parser.add_argument('--muestra', type=int, default=100, 
                        help='Tamaño de la muestra para validación')
    parser.add_argument('--evaluar', action='store_true',
                        help='Evaluar precisión con etiquetas manuales')
    
    args = parser.parse_args()
    
    if args.evaluar:
        evaluar_precision()
    else:
        crear_muestra_validacion(n_muestra=args.muestra)


if __name__ == "__main__":
    main()
