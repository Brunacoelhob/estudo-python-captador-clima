# Captador de Clima (OpenWeather + Excel)

[![CI](https://github.com/Brunacoelhob/estudo-python-captador-clima/actions/workflows/ci.yml/badge.svg)](https://github.com/Brunacoelhob/estudo-python-captador-clima/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

Aplicativo de janela (Tkinter) que consulta a **temperatura e a umidade** de uma cidade (padrão: São Paulo) na API da OpenWeather, guarda o histórico numa planilha Excel e mostra tabela, gráfico e **previsão de 5 dias**.

## Funcionalidades

- Login simples (nome e e-mail, validados) para identificar quem fez cada consulta
- **Consultar agora**: temperatura e umidade atuais, gravadas na planilha
- **Previsão de 5 dias** (mínima/máxima e umidade média por dia, com dados reais da API)
- **Histórico** das últimas 10 consultas e **gráfico** de variação
- Abrir a planilha no programa padrão (Windows, macOS e Linux)

## Como executar

Requer Python 3.10+ (com Tkinter, que já vem com o instalador oficial).

```bash
pip install -r requirements.txt
cp .env.example .env      # coloque sua chave em OPENWEATHER_API_KEY
python -m captador
```

Chave gratuita em https://openweathermap.org/api. Opcionais no `.env`: `CLIMA_CIDADE` (ex.: `Recife,BR`) e `CLIMA_PLANILHA`.

## Arquitetura

```
captador/
├── config.py        configuração (ambiente/.env); a chave nunca fica no código
├── clima.py         cliente da API: timeout, erros claros, previsão agrupada por dia
├── armazenamento.py planilha Excel: validação do usuário, gravação segura, últimos N
├── grafico.py       dados do gráfico (matplotlib só é carregado ao abrir o gráfico)
├── interface.py     telas Tkinter (sem regra de negócio)
└── __main__.py      ponto de entrada
tests/               27 testes (sem rede e sem interface gráfica)
```

## O que foi corrigido em relação à primeira versão

| Antes | Agora |
|---|---|
| **Chave da API escrita no código** (e publicada no GitHub) | Lida de `OPENWEATHER_API_KEY`; não aparece em logs/erros |
| "Previsão" com valores **inventados** (28°C, 23°C…) na tela | Previsão real de 5 dias da API |
| Requisição sem timeout nem checagem de status | Timeout, mensagens para 401/404/429/erro de rede |
| Planilha com dados pessoais versionada | `*.xlsx` no `.gitignore` |
| Nome digitado como `=HYPERLINK(...)` virava **fórmula** no Excel | "Injeção de fórmula" neutralizada |
| Planilha podia corromper se o programa fechasse ao salvar | Gravação atômica (arquivo temporário + troca) |
| `os.startfile` (só Windows) | Funciona em Windows, macOS e Linux |
| Tudo em um arquivo com variáveis globais | Pacote em módulos, testável |
| Sem validação de e-mail/nome, sem testes, sem CI | Validação, 27 testes e CI (ruff + pytest) |

## Privacidade

Nome e e-mail ficam **apenas na planilha local**, ao lado de cada consulta. Nada é enviado a terceiros além do pedido de clima (que contém só a cidade e a chave da API).

## Testes

```bash
pip install -r requirements-dev.txt
pytest
ruff check . && ruff format --check .
```

## Licença

[MIT](LICENSE)
