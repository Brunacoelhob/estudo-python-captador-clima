"""Interface gráfica (Tkinter). Toda a lógica está nos outros módulos; aqui só há telas."""

from __future__ import annotations

import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

import requests

from . import clima, grafico
from .armazenamento import DadosInvalidos, HistoricoPlanilha, Usuario
from .config import Configuracao

AZUL = "#2c5282"


class Aplicacao:
    def __init__(self, config: Configuracao) -> None:
        self.config = config
        self.historico = HistoricoPlanilha(config.arquivo_planilha)
        self.sessao = requests.Session()
        self.usuario: Usuario | None = None
        self.janela = tk.Tk()
        self.janela.title("Captador de Clima")
        self.tela_login()

    # ---------- telas ----------
    def _limpar(self, geometria: str) -> None:
        for widget in self.janela.winfo_children():
            widget.destroy()
        self.janela.geometry(geometria)
        self.janela.configure(bg="white")

    def _cabecalho(self, pai: tk.Misc, titulo: str, subtitulo: str = "") -> None:
        quadro = tk.Frame(pai, bg=AZUL)
        quadro.pack(fill="x")
        tk.Label(quadro, text=titulo, font=("Arial", 16, "bold"), bg=AZUL, fg="white", pady=8).pack()
        if subtitulo:
            tk.Label(quadro, text=subtitulo, font=("Arial", 11), bg=AZUL, fg="white").pack(pady=(0, 6))

    def tela_login(self) -> None:
        self._limpar("500x340")
        self._cabecalho(self.janela, "Login")
        conteudo = tk.Frame(self.janela, bg="white")
        conteudo.pack(pady=20)

        tk.Label(conteudo, text="Nome", anchor="w", font=("Arial", 12), bg="white").pack(fill="x")
        nome = tk.Entry(conteudo, font=("Arial", 12), width=40, relief="solid")
        nome.pack(pady=5)
        tk.Label(conteudo, text="E-mail", anchor="w", font=("Arial", 12), bg="white").pack(fill="x")
        email = tk.Entry(conteudo, font=("Arial", 12), width=40, relief="solid")
        email.pack(pady=5)
        tk.Label(
            conteudo,
            text="Seu nome e e-mail são gravados apenas na planilha local, junto de cada consulta.",
            font=("Arial", 9),
            bg="white",
            fg="#555",
        ).pack(pady=(4, 0))

        def entrar() -> None:
            try:
                self.usuario = Usuario.validar(nome.get(), email.get())
            except DadosInvalidos as erro:
                messagebox.showwarning("Atenção", str(erro))
                return
            self.tela_principal()

        tk.Button(
            conteudo, text="Iniciar", command=entrar, bg=AZUL, fg="white", font=("Arial", 12, "bold"), width=15, relief="flat"
        ).pack(pady=15)

    def tela_principal(self) -> None:
        self._limpar("600x520")
        self._cabecalho(self.janela, "Clima", self.config.cidade)
        botoes = tk.Frame(self.janela, bg="white")
        botoes.pack(pady=25)
        estilo = {"font": ("Arial", 14, "bold"), "width": 22, "height": 2, "bd": 0, "fg": "white"}
        tk.Button(botoes, text="Consultar agora", command=self.consultar, bg="#F9A825", **estilo).pack(pady=4)
        tk.Button(botoes, text="Previsão de 5 dias", command=self.previsao, bg="#388E3C", **estilo).pack(pady=4)
        tk.Button(botoes, text="Histórico", command=self.ver_historico, bg="#0288D1", **estilo).pack(pady=4)
        tk.Button(botoes, text="Gráfico", command=self.ver_grafico, bg="#7B1FA2", **estilo).pack(pady=4)
        tk.Button(botoes, text="Abrir planilha", command=self.abrir_planilha, bg="#546E7A", **estilo).pack(pady=4)
        tk.Button(
            self.janela,
            text="Sair da conta",
            command=self.tela_login,
            bg="gray",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
        ).pack(pady=8)

    def _tabela(self, titulo: str, subtitulo: str, colunas: list[str], linhas: list[list[str]]) -> None:
        janela = tk.Toplevel(self.janela)
        janela.title(titulo)
        janela.configure(bg="white")
        self._cabecalho(janela, titulo, subtitulo)
        tabela = tk.Frame(janela, bg="white")
        tabela.pack(padx=20, pady=15)
        for c, texto in enumerate(colunas):
            tk.Label(tabela, text=texto, font=("Arial", 10, "bold"), bg="#03A9F4", fg="white", width=18).grid(row=0, column=c)
        for i, linha in enumerate(linhas, start=1):
            for c, valor in enumerate(linha):
                tk.Label(tabela, text=valor, font=("Arial", 10), bg="white", width=18).grid(row=i, column=c)
        tk.Button(
            janela,
            text="OK",
            command=janela.destroy,
            bg="#4caf50",
            fg="white",
            font=("Arial", 10, "bold"),
            width=10,
            relief="flat",
        ).pack(pady=10)

    # ---------- ações ----------
    def consultar(self) -> None:
        try:
            leitura = clima.buscar_atual(self.sessao, self.config)
            assert self.usuario is not None
            self.historico.salvar(leitura, self.usuario)
        except clima.ErroClima as erro:
            messagebox.showerror("Erro", str(erro))
            return
        except OSError:
            messagebox.showerror("Erro", "Não foi possível gravar a planilha. Ela está aberta em outro programa?")
            return
        messagebox.showinfo("Clima agora", f"{leitura.temperatura:.1f} °C · umidade {leitura.umidade}%\n\nRegistro salvo.")

    def previsao(self) -> None:
        try:
            dias = clima.buscar_previsao(self.sessao, self.config)
        except clima.ErroClima as erro:
            messagebox.showerror("Erro", str(erro))
            return
        linhas = [[d.dia, f"{d.minima:.0f}° / {d.maxima:.0f}°C", f"{d.umidade_media}%"] for d in dias]
        self._tabela("Previsão de 5 dias", self.config.cidade, ["Dia", "Mín / Máx", "Umidade média"], linhas)

    def ver_historico(self) -> None:
        registros = self.historico.ultimos(10)
        if not registros:
            messagebox.showwarning("Aviso", "Nenhum dado salvo ainda.")
            return
        linhas = [[r.data_hora, f"{r.temperatura:.1f} °C", f"{r.umidade}%", r.nome, r.email] for r in registros]
        self._tabela("Histórico", "Últimas 10 consultas", ["Data/Hora", "Temperatura", "Umidade", "Nome", "E-mail"], linhas)

    def ver_grafico(self) -> None:
        registros = self.historico.ultimos(10)
        if not registros:
            messagebox.showwarning("Aviso", "Nenhum dado salvo ainda.")
            return
        grafico.mostrar(registros, self.config.cidade)

    def abrir_planilha(self) -> None:
        caminho = self.config.arquivo_planilha
        if not caminho.exists():
            messagebox.showwarning("Aviso", "A planilha ainda não foi criada.")
            return
        if sys.platform.startswith("win"):
            os.startfile(caminho)  # type: ignore[attr-defined]  # só existe no Windows
        elif sys.platform == "darwin":
            subprocess.run(["open", str(caminho)], check=False)
        else:
            subprocess.run(["xdg-open", str(caminho)], check=False)

    def executar(self) -> None:
        self.janela.mainloop()
