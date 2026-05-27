# ============================================================
#  ANÁLISIS DE VENTAS MENSUAL — Google Colab
#  Instrucciones:
#  1. Cloná tu repo con la celda de git clone (ver abajo)
#  2. Ajustá las variables de la sección CONFIGURACIÓN
#  3. Ejecutá todo (Runtime → Run all)
# ============================================================

# ── CELDA 1: Clonar repositorio ──────────────────────────────
# Reemplazá la URL con la de tu repo

# !git clone https://github.com/tu-usuario/tu-repo.git
# %cd tu-repo   # entrá a la carpeta del repo

# Si ya tenés el archivo subido directo a Colab, comentá las
# líneas de arriba y usá la ruta local del archivo.


# ── CELDA 2: Instalación de librerías (si hace falta) ────────
# En Colab ya vienen instaladas, pero por si acaso:
# !pip install matplotlib pandas --quiet


# ── CELDA 3: Importaciones ────────────────────────────────────
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ── CELDA 4: CONFIGURACIÓN — ¡editá esto! ────────────────────

ARCHIVO_CSV = "ventas.csv"          # ruta al CSV dentro del repo

# Nombres de las columnas en TU archivo CSV:
COL_FECHA       = "fecha"           # columna con la fecha de cada venta
COL_CANTIDAD    = "cantidad"        # columna con ítems vendidos por fila
COL_FACTURACION = "total"           # columna con el monto facturado por fila

# Formato de fecha (ejemplos comunes):
#   "%Y-%m-%d"  →  2024-03-15
#   "%d/%m/%Y"  →  15/03/2024
#   "%m/%d/%Y"  →  03/15/2024
FORMATO_FECHA = "%Y-%m-%d"

# Moneda para el eje de facturación
SIMBOLO_MONEDA = "$"

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

# ── Barras: ítems vendidos (eje izquierdo) ──
barras1 = ax1.bar(
    x - ancho / 2,
    resumen["items_vendidos"],
    width=ancho,
    color=COLOR_ITEMS,
    alpha=0.88,
    label="Ítems vendidos",
    zorder=3,
)

# ── Línea + área: facturación (eje derecho) ──
ax2 = ax1.twinx()
ax2.plot(
    x,
    resumen["facturacion"],
    color=COLOR_FACT,
    linewidth=2.5,
    marker="o",
    markersize=7,
    label="Facturación",
    zorder=4,
)
ax2.fill_between(
    x,
    resumen["facturacion"],
    alpha=0.12,
    color=COLOR_FACT,
    zorder=2,
)

# Barras fantasma para la leyenda conjunta
barra_fact = plt.Rectangle((0, 0), 1, 1, fc=COLOR_FACT, alpha=0.7)

# ── Etiquetas sobre las barras ──
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
plt.savefig("ventas_mensuales.png", dpi=150, bbox_inches="tight")
plt.show()
print("📊 Gráfico guardado como ventas_mensuales.png")
