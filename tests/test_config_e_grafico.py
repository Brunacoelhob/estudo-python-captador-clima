from pathlib import Path

import pytest

from captador.armazenamento import Registro
from captador.config import ErroDeConfiguracao, carregar
from captador.grafico import serie


def test_chave_da_api_e_obrigatoria_e_a_mensagem_orienta():
    with pytest.raises(ErroDeConfiguracao, match="OPENWEATHER_API_KEY"):
        carregar(ambiente={}, dotenv=None)
    with pytest.raises(ErroDeConfiguracao):
        carregar(ambiente={"OPENWEATHER_API_KEY": "   "}, dotenv=None)


def test_valores_padrao_e_personalizados():
    c = carregar(ambiente={"OPENWEATHER_API_KEY": "k"}, dotenv=None)
    assert c.cidade == "Sao Paulo,BR" and c.arquivo_planilha == Path("dados_clima.xlsx")

    c = carregar(ambiente={"OPENWEATHER_API_KEY": "k", "CLIMA_CIDADE": "Recife,BR", "CLIMA_PLANILHA": "x.xlsx"}, dotenv=None)
    assert c.cidade == "Recife,BR" and c.arquivo_planilha == Path("x.xlsx")


def test_le_arquivo_dotenv_e_ambiente_tem_prioridade(tmp_path):
    env = tmp_path / ".env"
    env.write_text('# comentário\nOPENWEATHER_API_KEY="da-chave-no-arquivo"\nCLIMA_CIDADE=Curitiba,BR\n', encoding="utf-8")

    assert carregar(ambiente={}, dotenv=env).chave_api == "da-chave-no-arquivo"
    assert carregar(ambiente={"OPENWEATHER_API_KEY": "do-ambiente"}, dotenv=env).chave_api == "do-ambiente"
    assert carregar(ambiente={}, dotenv=env).cidade == "Curitiba,BR"


def test_a_chave_nao_aparece_no_repr():
    c = carregar(ambiente={"OPENWEATHER_API_KEY": "SEGREDO-XYZ"}, dotenv=None)
    assert "SEGREDO-XYZ" not in repr(c)


def test_serie_do_grafico():
    registros = [Registro("08/04/2026 10:00", 20.26, 60, "A", "a@b.co"), Registro("08/04/2026 11:00", 21.0, 55, "A", "a@b.co")]
    datas, temps, umids = serie(registros)
    assert datas == ["08/04/2026\n10:00", "08/04/2026\n11:00"]
    assert temps == [20.3, 21.0] and umids == [60, 55]
