#Captação de Temperatura - São Paulo
Este projeto tem como objetivo automatizar a coleta de dados de temperatura e umidade do ar da
cidade de São Paulo - SP, utilizando a API da OpenWeather e salvando os dados localmente com
interface gráfica e visual moderna.

---

## Funcionalidades
- Tela de login inicial com entrada de nome e e-mail
- Obter dados de temperatura atual e umidade do ar
- Salvar os dados automaticamente em uma planilha Excel (dados_clima.xlsx)
- Visualizar o histórico em uma tabela com interface gráfica
- Gerar gráfico com a variação de temperatura e umidade (últimos 10 registros)
- Exportar a planilha e abrir diretamente no Excel
- Botões estilizados e responsivos
- Design unificado e intuitivo
- Integração dos dados com o nome e e-mail do usuário que fez a consulta

---

## Tecnologias Utilizadas
- Python 3.10+
- Tkinter (interface gráfica)
- OpenWeather API (coleta dos dados meteorológicos)
- openpyxl (leitura e escrita em planilhas Excel)
- matplotlib (geração de gráficos)
- os, datetime, requests

---

# Pré-requisitos
Antes de rodar o projeto, você precisa ter:
- Python 3.10 ou superior instalado
- pip (gerenciador de pacotes Python)
Instale as bibliotecas com o comando:
pip install requests openpyxl matplotlib

Como executar o projeto
1. Clone o repositório ou baixe os arquivos do projeto
2. Execute o arquivo main.py
3. Preencha seu nome e e-mail
4. Use os botões para:
- Buscar previsão
- Visualizar dados
- Gerar gráfico
- Abrir planilha
5. Visualize os dados e gráfico em tempo real!

Organização do Projeto
main.py - Arquivo principal da aplicação
dados_clima.xlsx - Planilha gerada automaticamente
README.md - Documentação do projeto
imagens/ - Capturas da interface (opcional)
docs/ - Fluxograma, roteiro de apresentação (opcional)

Melhorias Futuras
- Envio automático da planilha por e-mail
- Escolher cidade para consulta além de São Paulo
- Armazenamento dos dados em banco de dados (SQLite ou PostgreSQL)
- Dashboard web com gráficos em tempo real


Autor
Desenvolvido por Bruna Coelho
Projeto acadêmico | FECAF | ADS - 2025
GitHub: https://github.com/Brunacoelhoh
API
OpenWeather: https://openweathermap.org/api
