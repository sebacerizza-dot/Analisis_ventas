import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

# Definir rutas de archivos de forma robusta
SCRIPT_DIR = os.path.dirname(__file__)
ARCHIVO_CSV = os.path.join(SCRIPT_DIR, '..', 'datos', 'ventas_2025.csv')
ARCHIVO_SALIDA = os.path.join(SCRIPT_DIR, '..', 'resultados', 'ventas_mensuales.png')

# Nombres de las columnas en TU archivo CSV:
COL_FECHA       = "fecha"           # columna con la fecha de cada venta
COL_CANTIDAD    = "cantidad"        # columna con ítems vendidos por fila
COL_FACTURACION = "precio_total"    # columna con el monto facturado por fila

# Formato de fecha (ejemplos comunes):
#   "%Y-%m-%d"  →  2024-03-15
#   "%d/%m/%Y"  →  15/03/2024
#   "%m/%d/%Y"  →  03/15/2024
FORMATO_FECHA = "%Y-%m-%d"

# Moneda para el eje de facturación
SIMBOLO_MONEDA = "$"

try:
    # ── CELDA 5: Carga y preparación de datos ────────────────────
    df = pd.read_csv(ARCHIVO_CSV)

    # Convertir fecha y extraer mes
    df[COL_FECHA] = pd.to_datetime(df[COL_FECHA], format=FORMATO_FECHA)
    df["mes"]     = df[COL_FECHA].dt.to_period("M")

    # Agrupar por mes
    resumen = (
        df.groupby("mes")
        .agg(
            items_vendidos  = (COL_CANTIDAD,    "sum"),
            facturacion     = (COL_FACTURACION, "sum"),
        )
        .reset_index()
        .sort_values("mes")
    )

    # Etiquetas de mes en español
    MESES_ES = {
        1:"Ene", 2:"Feb", 3:"Mar", 4:"Abr",
        5:"May", 6:"Jun", 7:"Jul", 8:"Ago",
        9:"Sep", 10:"Oct", 11:"Nov", 12:"Dic"
    }
    resumen["etiqueta"] = resumen["mes"].apply(
        lambda p: MESES_ES.get(p.month, str(p))
    )

    print("✅ Datos cargados correctamente")
    print(resumen[["etiqueta","items_vendidos","facturacion"]].to_string(index=False))


    # ── CELDA 6: Gráfico ─────────────────────────────────────────
    x      = np.arange(len(resumen))
    ancho  = 0.38

    # Paleta de colores
    COLOR_ITEMS = "#2563EB"   # azul
    COLOR_FACT  = "#16A34A"   # verde

    fig, ax1 = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor("#F8FAFC")
    ax1.set_facecolor("#F8FAFC")

    # Barras para ítems vendidos
    barras1 = ax1.bar(x - ancho/2, resumen["items_vendidos"], ancho, label="Ítems vendidos", color=COLOR_ITEMS, zorder=3)

    # Línea para facturación
    ax2 = ax1.twinx()
    ax2.plot(x + ancho/2, resumen["facturacion"], color=COLOR_FACT, marker="o", markersize=7, linewidth=2.5, label="Facturación", zorder=3)

    # Etiquetas sobre las barras de ítems vendidos
    for bar in barras1:
        h = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            h + max(resumen["items_vendidos"]) * 0.015,
            f"{int(h):,}".replace(",", "."),
            ha="center", va="bottom",
            fontsize=8.5, color=COLOR_ITEMS, fontweight="bold"
        )

    # Etiquetas sobre los puntos de facturación
    for xi, val in zip(x, resumen["facturacion"]):
        ax2.text(
            xi,
            val + max(resumen["facturacion"]) * 0.02,
            f"{SIMBOLO_MONEDA}{val:,.0f}".replace(",", "."),
            ha="center", va="bottom",
            fontsize=8, color=COLOR_FACT, fontweight="bold"
        )

    # ── Formato ejes ──
    ax1.set_xlabel("Mes", fontsize=12, labelpad=8)
    ax1.set_ylabel("Ítems vendidos", fontsize=12, color=COLOR_ITEMS, labelpad=8)
    ax2.set_ylabel(f"Facturación ({SIMBOLO_MONEDA})", fontsize=12, color=COLOR_FACT, labelpad=8)

    ax1.set_xticks(x)
    ax1.set_xticklabels(resumen["etiqueta"], fontsize=11)
    ax1.tick_params(axis="y", labelcolor=COLOR_ITEMS)
    ax2.tick_params(axis="y", labelcolor=COLOR_FACT)

    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda v, _: f"{int(v):,}".replace(",", ".")
    ))
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda v, _: f"{SIMBOLO_MONEDA}{v:,.0f}".replace(",", ".")
    ))

    ax1.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
    ax1.set_axisbelow(True)

    # ── Leyenda y título ──
    handles = [
        plt.Rectangle((0,0),1,1, fc=COLOR_ITEMS, alpha=0.88),
        plt.Line2D([0],[0], color=COLOR_FACT, linewidth=2.5,
                   marker="o", markersize=7),
    ]
    ax1.legend(
        handles,
        ["Ítems vendidos", "Facturación"],
        loc="upper left",
        framealpha=0.9,
        fontsize=10,
    )

    año = resumen["mes"].iloc[0].year
    plt.title(
        f"Ventas mensuales — {año}",
        fontsize=16, fontweight="bold", pad=16
    )

    plt.tight_layout()

    # Crear el directorio de resultados si no existe
    output_dir = os.path.dirname(ARCHIVO_SALIDA)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.savefig(ARCHIVO_SALIDA, dpi=150, bbox_inches="tight")
    print(f"📊 Gráfico guardado en {ARCHIVO_SALIDA}")
    plt.show()
    print("📊 Gráfico guardado como ventas_mensuales.png")

except FileNotFoundError:
    print(f"Error: El archivo '{ARCHIVO_CSV}' no se encontró. Asegúrate de que la ruta sea correcta.")
except KeyError as e:
    print(f"Error: Columna no encontrada - {e}. Asegúrate de que las columnas 'fecha', 'cantidad' y 'precio_total' existan.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
