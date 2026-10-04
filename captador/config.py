"""Configuração lida do ambiente (ou de um arquivo .env). Nenhum segredo fica no código-fonte."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path


class ErroDeConfiguracao(RuntimeError):
    """Configuração ausente ou inválida; a mensagem diz o que fazer."""


@dataclass(frozen=True)
class Configuracao:
    chave_api: str = field(repr=False)  # repr=False: a chave não aparece em logs nem em tracebacks
    cidade: str = "Sao Paulo,BR"
    arquivo_planilha: Path = Path("dados_clima.xlsx")
    timeout_segundos: float = 10.0


def _ler_dotenv(caminho: Path) -> dict[str, str]:
    """Lê linhas CHAVE=valor de um .env simples (sem dependência extra)."""
    valores: dict[str, str] = {}
    if not caminho.is_file():
        return valores
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, _, valor = linha.partition("=")
        valores[chave.strip()] = valor.strip().strip('"').strip("'")
    return valores


def carregar(ambiente: Mapping[str, str] | None = None, dotenv: Path | None = Path(".env")) -> Configuracao:
    """Variáveis de ambiente têm prioridade sobre o .env."""
    fonte: dict[str, str] = {}
    if dotenv is not None:
        fonte.update(_ler_dotenv(dotenv))
    fonte.update(os.environ if ambiente is None else ambiente)

    chave = fonte.get("OPENWEATHER_API_KEY", "").strip()
    if not chave:
        raise ErroDeConfiguracao(
            "Defina OPENWEATHER_API_KEY (variável de ambiente ou arquivo .env). "
            "Crie uma chave gratuita em https://openweathermap.org/api e veja o .env.example."
        )
    return Configuracao(
        chave_api=chave,
        cidade=fonte.get("CLIMA_CIDADE", "Sao Paulo,BR").strip() or "Sao Paulo,BR",
        arquivo_planilha=Path(fonte.get("CLIMA_PLANILHA", "dados_clima.xlsx")),
    )
