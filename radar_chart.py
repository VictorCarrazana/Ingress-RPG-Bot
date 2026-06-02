import matplotlib.pyplot as plt
import numpy as np


def create_radar_chart(results, agent_name):

    # =========================
    # DATOS
    # =========================

    labels = list(results.keys())
    values = list(results.values())

    # cerrar círculo
    values += values[:1]

    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False
    ).tolist()

    angles += angles[:1]

    # =========================
    # FIGURA
    # =========================

    fig, ax = plt.subplots(
        figsize=(9, 9),
        subplot_kw=dict(polar=True)
    )

    # =========================
    # COLORES CYBERPUNK
    # =========================

    neon_color = "#00F5FF"

    # fondo general
    fig.patch.set_facecolor("#02040A")

    # fondo radar
    ax.set_facecolor("#071018")

    # =========================
    # GRID
    # =========================

    ax.grid(
        color=neon_color,
        linestyle=(0, (4, 6)),
        linewidth=1,
        alpha=0.22
    )

    # borde exterior
    ax.spines["polar"].set_color(neon_color)
    ax.spines["polar"].set_linewidth(2)

    # =========================
    # GLOW EXTERIOR
    # =========================

    for width, alpha in [
        (20, 0.03),
        (15, 0.05),
        (10, 0.08),
        (7, 0.12),
    ]:

        ax.plot(
            angles,
            values,
            color=neon_color,
            linewidth=width,
            alpha=alpha,
            solid_capstyle="round",
            zorder=1
        )

    # =========================
    # LINEA PRINCIPAL
    # =========================

    ax.plot(
        angles,
        values,
        color=neon_color,
        linewidth=3.5,
        solid_capstyle="round",
        zorder=5
    )

    # =========================
    # PUNTOS NEON
    # =========================

    # glow grande
    ax.scatter(
        angles[:-1],
        values[:-1],
        s=500,
        color=neon_color,
        alpha=0.08,
        zorder=4
    )

    # punto principal
    ax.scatter(
        angles[:-1],
        values[:-1],
        s=120,
        color=neon_color,
        zorder=6
    )

    # =========================
    # RELLENO
    # =========================

    ax.fill(
        angles,
        values,
        color=neon_color,
        alpha=0.15,
        zorder=2
    )

    # =========================
    # ETIQUETAS
    # =========================

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(
        [label.upper() for label in labels],
        fontsize=12,
        fontweight="bold",
        color="#7DF9FF"
    )

    # =========================
    # ESCALA
    # =========================

    ax.set_ylim(0, 100)

    ax.set_yticks([20, 40, 60, 80, 100])

    ax.set_yticklabels(
        ["20", "40", "60", "80", "100"],
        color="#4FDFFF",
        fontsize=9
    )

    # =========================
    # CIRCULO EXTERIOR EXTRA
    # =========================

    ax.plot(
        np.linspace(0, 2*np.pi, 500),
        [100]*500,
        color=neon_color,
        linewidth=2,
        alpha=0.25
    )

    # =========================
    # TITULO
    # =========================

    plt.title(
        f"{agent_name.upper()} ",
        size=22,
        color=neon_color,
        fontweight="bold",
        pad=30
    )

    # =========================
    # GUARDAR
    # =========================

    filename = "radar_chart.png"

    plt.savefig(
        filename,
        bbox_inches="tight",
        facecolor=fig.get_facecolor(),
        dpi=300
    )

    plt.close()

    return filename
