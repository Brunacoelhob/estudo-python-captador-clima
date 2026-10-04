"""Ponto de entrada: python -m captador"""

from __future__ import annotations

import sys

from .config import ErroDeConfiguracao, carregar


def main() -> int:
    try:
        config = carregar()
    except ErroDeConfiguracao as erro:
        print(f"Erro de configuração: {erro}", file=sys.stderr)
        return 1

    from .interface import Aplicacao  # importado aqui para que o Tkinter só seja exigido ao abrir a janela

    Aplicacao(config).executar()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
