"""Acesso à API OpenWeather: leitura atual e previsão de 5 dias (dados reais, nada inventado)."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Protocol

from .config import Configuracao

URL_ATUAL = "https://api.openweathermap.org/data/2.5/weather"
URL_PREVISAO = "https://api.openweathermap.org/data/2.5/forecast"
DIAS_SEMANA = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]


class ErroClima(RuntimeError):
    """Falha ao obter dados do clima; a mensagem é segura para mostrar ao usuário."""


class Sessao(Protocol):
    """O que usamos de `requests.Session` (permite trocar por um falso nos testes)."""

    def get(self, url: str, *, params: dict[str, Any], timeout: float) -> Any: ...


@dataclass(frozen=True)
class Leitura:
    temperatura: float
    umidade: int


@dataclass(frozen=True)
class PrevisaoDia:
    dia: str  # "Seg 08/04"
    minima: float
    maxima: float
    umidade_media: int


def _consultar(sessao: Sessao, url: str, config: Configuracao) -> dict[str, Any]:
    parametros = {"q": config.cidade, "appid": config.chave_api, "units": "metric", "lang": "pt_br"}
    try:
        resposta = sessao.get(url, params=parametros, timeout=config.timeout_segundos)
    except Exception:  # rede fora, DNS, timeout... (o tipo exato depende da biblioteca)
        # Não repassa `erro` na mensagem: a URL da requisição conteria a chave da API.
        raise ErroClima("Não foi possível conectar ao serviço de clima. Verifique a internet.") from None

    if resposta.status_code == 401:
        raise ErroClima("Chave da API rejeitada (401). Confira OPENWEATHER_API_KEY.")
    if resposta.status_code == 404:
        raise ErroClima(f"Cidade não encontrada: {config.cidade}.")
    if resposta.status_code == 429:
        raise ErroClima("Limite de consultas da API atingido (429). Tente novamente mais tarde.")
    if resposta.status_code != 200:
        raise ErroClima(f"O serviço de clima respondeu com erro ({resposta.status_code}).")
    try:
        dados = resposta.json()
    except ValueError:
        raise ErroClima("Resposta inválida do serviço de clima.") from None
    if not isinstance(dados, dict):
        raise ErroClima("Resposta inválida do serviço de clima.")
    return dados


def buscar_atual(sessao: Sessao, config: Configuracao) -> Leitura:
    dados = _consultar(sessao, URL_ATUAL, config)
    try:
        principal = dados["main"]
        return Leitura(temperatura=float(principal["temp"]), umidade=int(principal["humidity"]))
    except (KeyError, TypeError, ValueError):
        raise ErroClima("A resposta do serviço de clima veio sem temperatura/umidade.") from None


def agrupar_por_dia(itens: list[dict[str, Any]]) -> list[PrevisaoDia]:
    """A API devolve medições de 3 em 3 horas; aqui viram mínima/máxima/umidade média por dia."""
    por_dia: dict[str, list[tuple[float, float, int]]] = defaultdict(list)
    ordem: list[str] = []
    for item in itens:
        try:
            momento = datetime.fromtimestamp(int(item["dt"]))
            principal = item["main"]
            medida = (float(principal["temp_min"]), float(principal["temp_max"]), int(principal["humidity"]))
        except (KeyError, TypeError, ValueError):
            continue  # medição malformada é ignorada, não derruba a tela
        chave = f"{DIAS_SEMANA[momento.weekday()]} {momento:%d/%m}"
        if chave not in por_dia:
            ordem.append(chave)
        por_dia[chave].append(medida)

    return [
        PrevisaoDia(
            dia=chave,
            minima=min(m[0] for m in por_dia[chave]),
            maxima=max(m[1] for m in por_dia[chave]),
            umidade_media=round(sum(m[2] for m in por_dia[chave]) / len(por_dia[chave])),
        )
        for chave in ordem
    ]


def buscar_previsao(sessao: Sessao, config: Configuracao) -> list[PrevisaoDia]:
    dados = _consultar(sessao, URL_PREVISAO, config)
    itens = dados.get("list")
    if not isinstance(itens, list):
        raise ErroClima("A resposta da previsão veio em formato inesperado.")
    return agrupar_por_dia(itens)
