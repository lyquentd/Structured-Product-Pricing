import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
IMAGES_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Colors
C_BOX = 'white'
C_EDGE = 'black'
C_EMISSION = '#ff8c00'  # Orange
C_MATURITY = '#8b0000'  # Brown

# Helper to draw boxes
def draw_box(x, y, text, width=2.2, height=0.8, fontsize=12):
    rect = patches.Rectangle((x - width/2, y - height/2), width, height, 
                             linewidth=1.2, edgecolor=C_EDGE, facecolor=C_BOX, zorder=3)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, fontweight='bold', zorder=4)

# Define node positions
pos = {
    'Client': (5, 8.5),
    'Emetteur': (5, 6),
    'Structureur': (5, 3),
    'Trader 1\n(Taux)': (1.5, 3),
    'Trader 2\n(Equity)': (8.5, 3)
}

# Draw Nodes
for k, v in pos.items():
    draw_box(v[0], v[1], k)

# Helper for arrows without automatic text
def draw_arrow(x1, y1, x2, y2, color, curve=0):
    if curve != 0:
        patch = patches.FancyArrowPatch((x1, y1), (x2, y2), 
                                      connectionstyle=f"arc3,rad={curve}", 
                                      color=color, arrowstyle="-|>", mutation_scale=15, lw=1.5, zorder=2)
    else:
        patch = patches.FancyArrowPatch((x1, y1), (x2, y2), 
                                      color=color, arrowstyle="-|>", mutation_scale=15, lw=1.5, zorder=2)
    ax.add_patch(patch)

# Helper for text
def draw_label(x, y, text, color):
    ax.text(x, y, text, color=color, ha='center', va='center', 
            fontsize=10, fontweight='bold', 
            bbox=dict(facecolor='white', edgecolor=color, boxstyle='square,pad=0.3'), zorder=5)

# ================================
# 1. EMISSION (Orange)
# ================================
# Client -> Emetteur
draw_arrow(4.8, 8.1, 4.8, 6.4, C_EMISSION)
draw_label(4.4, 7.25, "100", C_EMISSION)

# Emetteur -> Structureur
draw_arrow(4.8, 5.6, 4.8, 3.4, C_EMISSION)
draw_label(4.35, 4.5, "97.12\n(Produit)", C_EMISSION)

# Structureur -> Trader 1 (Taux)
draw_arrow(3.8, 3.1, 2.7, 3.1, C_EMISSION, curve=-0.3)
draw_label(3.25, 3.6, "76.12", C_EMISSION)

# Structureur -> Trader 2 (Equity)
draw_arrow(6.2, 3.1, 7.3, 3.1, C_EMISSION, curve=0.3)
draw_label(6.75, 3.6, "21.01", C_EMISSION)

# Marge Bank (Self-loop or text near Emetteur)
draw_label(3.0, 5.5, "Marge: 2.88\n(Conservée)", C_EMISSION)
ax.plot([4.8, 3.0], [5.6, 5.1], color=C_EMISSION, linestyle=':', zorder=1)


# ================================
# 2. MATURITY (Brown)
# ================================
# Emetteur -> Client
draw_arrow(5.2, 6.4, 5.2, 8.1, C_MATURITY)
draw_label(5.8, 7.25, "100 + Flux", C_MATURITY)

# Structureur -> Emetteur
draw_arrow(5.2, 3.4, 5.2, 5.6, C_MATURITY)
draw_label(6.0, 4.5, "100 + Flux\n(Performances)", C_MATURITY)

# Trader 1 -> Structureur
draw_arrow(2.7, 2.9, 3.8, 2.9, C_MATURITY, curve=-0.3)
draw_label(3.25, 2.4, "100\n(Remboursement ZC)", C_MATURITY)

# Trader 2 -> Structureur
draw_arrow(7.3, 2.9, 6.2, 2.9, C_MATURITY, curve=0.3)
draw_label(6.75, 2.4, "Flux des Options\nmax(0, ...)", C_MATURITY)

# Legend
ax.text(0.5, 9.5, "Flux à l'émission", color=C_EMISSION, fontweight='bold', fontsize=12)
ax.text(0.5, 9.0, "Flux à l'échéance", color=C_MATURITY, fontweight='bold', fontsize=12)
ax.plot([0.1, 0.4], [9.55, 9.55], color=C_EMISSION, lw=2)
ax.plot([0.1, 0.4], [9.05, 9.05], color=C_MATURITY, lw=2)

plt.title("Schéma de Structuration - ENERGETIC", fontweight='bold', fontsize=16)
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, "flow_diagram.png"), dpi=300)
plt.close()
