"""Gráfico de variação de temperatura e umidade."""

from __future__ import annotations

from .armazenamento import Registro


def serie(registros: list[Registro]) -> tuple[list[str], list[float], list[int]]:
    """Separa os registros em eixos (datas, temperaturas, umidades) prontos para plotar."""
    datas = [r.data_hora.replace(" ", "\n") for r in registros]
    return datas, [round(r.temperatura, 1) for r in registros], [r.umidade for r in registros]


def mostrar(registros: list[Registro], cidade: str) -> None:
    # matplotlib é importado só aqui: carregá-lo é lento e os testes não precisam dele.
    import matplotlib.pyplot as plt

    datas, temperaturas, umidades = serie(registros)
    plt.figure(figsize=(12, 5))
    plt.plot(datas, temperaturas, label="Temperatura (°C)", marker="o", linewidth=2, color="royalblue")
    plt.plot(datas, umidades, label="Umidade (%)", marker="o", linewidth=2, color="gray")
    plt.suptitle(
        f"Variação de temperatura e umidade\n{cidade}",
        fontsize=14,
        fontweight="bold",
        color="white",
        bbox={"facecolor": "#2c5282", "edgecolor": "none", "boxstyle": "round,pad=0.5"},
    )
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.xlabel("Data e hora")
    plt.ylabel("Valores")
    plt.legend()
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.show()
