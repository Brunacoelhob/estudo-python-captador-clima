from datetime import datetime

import pytest

from captador import clima
from captador.config import Configuracao

CONFIG = Configuracao(chave_api="CHAVE-SECRETA-123")


class RespostaFalsa:
    def __init__(self, status=200, corpo=None, json_invalido=False):
        self.status_code = status
        self._corpo = corpo
        self._json_invalido = json_invalido

    def json(self):
        if self._json_invalido:
            raise ValueError("não é json")
        return self._corpo


class SessaoFalsa:
    def __init__(self, resposta=None, erro=None):
        self.resposta, self.erro, self.chamadas = resposta, erro, []

    def get(self, url, *, params, timeout):
        self.chamadas.append((url, params, timeout))
        if self.erro:
            raise self.erro
        return self.resposta


def sessao(status=200, corpo=None, **kw):
    return SessaoFalsa(RespostaFalsa(status, corpo, **kw))


def test_busca_atual_devolve_temperatura_e_umidade():
    s = sessao(corpo={"main": {"temp": 23.46, "humidity": 71}})
    leitura = clima.buscar_atual(s, CONFIG)
    assert leitura == clima.Leitura(23.46, 71)


def test_requisicao_usa_timeout_chave_e_cidade_da_configuracao():
    s = sessao(corpo={"main": {"temp": 20, "humidity": 50}})
    clima.buscar_atual(s, CONFIG)
    url, params, timeout = s.chamadas[0]
    assert url == clima.URL_ATUAL
    assert params["appid"] == "CHAVE-SECRETA-123" and params["q"] == "Sao Paulo,BR" and params["units"] == "metric"
    assert timeout == CONFIG.timeout_segundos  # sem timeout o programa poderia travar para sempre


@pytest.mark.parametrize(
    "status,trecho", [(401, "Chave"), (404, "Cidade não encontrada"), (429, "Limite"), (500, r"erro \(500\)")]
)
def test_erros_http_viram_mensagens_claras(status, trecho):
    with pytest.raises(clima.ErroClima, match=trecho):
        clima.buscar_atual(sessao(status=status, corpo={}), CONFIG)


def test_falha_de_rede_nao_vaza_a_chave_da_api():
    # Exceções de requests costumam trazer a URL completa (com appid=...) na mensagem.
    s = SessaoFalsa(erro=ConnectionError("falha em https://api...?appid=CHAVE-SECRETA-123"))
    with pytest.raises(clima.ErroClima) as e:
        clima.buscar_atual(s, CONFIG)
    assert "CHAVE-SECRETA-123" not in str(e.value)
    assert "CHAVE-SECRETA-123" not in repr(e.value.__cause__)
    assert "internet" in str(e.value)


def test_json_invalido_ou_incompleto():
    with pytest.raises(clima.ErroClima, match="inválida"):
        clima.buscar_atual(sessao(json_invalido=True), CONFIG)
    with pytest.raises(clima.ErroClima, match="inválida"):
        clima.buscar_atual(sessao(corpo=[1, 2]), CONFIG)
    with pytest.raises(clima.ErroClima, match="sem temperatura"):
        clima.buscar_atual(sessao(corpo={"main": {}}), CONFIG)
    with pytest.raises(clima.ErroClima, match="sem temperatura"):
        clima.buscar_atual(sessao(corpo={"main": {"temp": "abc", "humidity": 1}}), CONFIG)


def _item(ano, mes, dia, hora, tmin, tmax, umid):
    return {"dt": int(datetime(ano, mes, dia, hora).timestamp()), "main": {"temp_min": tmin, "temp_max": tmax, "humidity": umid}}


def test_previsao_agrupa_medicoes_de_3_em_3_horas_por_dia():
    itens = [
        _item(2026, 4, 8, 9, 18.0, 20.0, 60),
        _item(2026, 4, 8, 15, 22.0, 27.5, 40),
        _item(2026, 4, 9, 9, 17.0, 19.0, 80),
    ]
    dias = clima.agrupar_por_dia(itens)
    assert [d.dia for d in dias] == ["Qua 08/04", "Qui 09/04"]
    assert (dias[0].minima, dias[0].maxima, dias[0].umidade_media) == (18.0, 27.5, 50)
    assert (dias[1].minima, dias[1].maxima, dias[1].umidade_media) == (17.0, 19.0, 80)


def test_previsao_ignora_medicao_malformada_sem_derrubar():
    itens = [_item(2026, 4, 8, 9, 18, 20, 60), {"dt": "x"}, {"main": {}}, None]
    assert len(clima.agrupar_por_dia(itens)) == 1


def test_previsao_via_api_e_formato_inesperado():
    corpo = {"list": [_item(2026, 4, 8, 9, 18, 20, 60)]}
    assert len(clima.buscar_previsao(sessao(corpo=corpo), CONFIG)) == 1
    with pytest.raises(clima.ErroClima, match="inesperado"):
        clima.buscar_previsao(sessao(corpo={"list": "oi"}), CONFIG)
