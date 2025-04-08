# Captação de Temperatura - São Paulo

Este projeto tem como objetivo automatizar a coleta de dados de **temperatura** e **umidade do ar** da cidade de **São Paulo - SP** utilizando a API da [OpenWeather](https://openweathermap.org/). Os dados são salvos automaticamente em uma planilha Excel e podem ser visualizados em uma interface gráfica desenvolvida com `Tkinter`.

---

## Funcionalidades

- Obter dados de **temperatura atual** e **umidade do ar**
- **Salvar os dados** automaticamente em uma planilha (`dados_clima.xlsx`)
- **Visualizar o histórico** de forma tabular com interface gráfica
- **Gerar gráficos** com a variação de temperatura e umidade
- Interface moderna com **design responsivo e intuitivo**

---

## Pré-requisitos

Antes de rodar o projeto, você precisa ter instalado:

- Python 3.10+
- pip (gerenciador de pacotes Python)

---

## Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/captador-temperatura.git

Acesse a pasta do projeto
cd captador-temperatura

Instale as dependências
pip install requests openpyxl matplotlib

Como obter a chave da API (OpenWeather)
Crie uma conta gratuita no site: https://openweathermap.org/

Vá em API Keys e gere sua chave

Copie sua chave e substitua no código:
chave_api = "SUA_CHAVE_AQUI"


Como executar o projeto
python index.py

A interface será aberta com as opções:

Buscar previsão (coleta e salva os dados)

Visualizar dados (exibe a planilha de forma gráfica)

Gerar gráfico (mostra a variação ao longo do tempo)

Captura de tela
Tela Principal:

Visualização de Dados:

Gráfico:

Tecnologias Utilizadas
Python 3

Tkinter (GUI)

OpenWeather API

openpyxl (planilhas Excel)

matplotlib (gráficos)


├── index.py               # Código principal
├── dados_clima.xlsx       # Planilha gerada automaticamente
├── README.md              # Documentação do projeto
├── assets/                # Imagens do projeto
└── requirements.txt       # (opcional)



Autor
Bruna Coelho

Licença
Este projeto está sob a licença MIT. Sinta-se livre para usar, modificar e compartilhar.



