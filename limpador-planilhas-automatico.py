import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re

janela = tk.Tk()
janela.title("Limpador de Planilhas PRO - v2.0")
janela.geometry("480x560")
janela.configure(bg="#f0f0f0")

tk.Label(janela, text="🧹 Limpador de Planilhas PRO", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=12)
tk.Label(janela, text="Limpa + Gera relatório para o chefe", bg="#f0f0f0").pack()

arquivo_escolhido = tk.StringVar(value="Nenhum arquivo escolhido")
tk.Label(janela, textvariable=arquivo_escolhido, bg="#f0f0f0", wraplength=420, fg="gray").pack(pady=8)

# Caixinha do relatório
relatorio_label = tk.Label(janela, text="Relatório vai aparecer aqui...", bg="white", justify="left", anchor="nw", font=("Consolas", 10), wraplength=420)
relatorio_label.pack(pady=10, padx=20, fill="both", expand=True)

def escolher_arquivo():
    arquivo = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx *.xls")])
    if arquivo:
        arquivo_escolhido.set(arquivo)

def limpar_telefone(s):
    if pd.isna(s) or str(s).strip() == "":
        return s, False
    so_numero = ''.join([c for c in str(s) if c.isdigit()])
    if len(so_numero) == 10:
        return f"({so_numero[:2]}) {so_numero[2:6]}-{so_numero[6:]}", True
    if len(so_numero) == 11:
        return f"({so_numero[:2]}) {so_numero[2:7]}-{so_numero[7:]}", True
    return s, False

def limpar():
    caminho = arquivo_escolhido.get()
    if "Nenhum" in caminho or not caminho:
        messagebox.showwarning("Ops!", "Escolha um arquivo primeiro!")
        return
    try:
        df = pd.read_excel(caminho)
        linhas_antes = len(df)
        colunas = len(df.columns)

        # Contadores do relatório
        vazias_removidas = 0
        duplicados_removidos = 0
        telefones_arrumados = 0
        nomes_arrumados = 0
        datas_arrumadas = 0

        # 1. Tirar linhas totalmente vazias
        antes = len(df)
        df = df.dropna(how='all')
        vazias_removidas = antes - len(df)

        # 2. Limpar nome das colunas
        df.columns = [str(c).strip() for c in df.columns]

        # 3. Limpar textos, telefones e nomes
        for col in df.select_dtypes(include='object').columns:
            # Telefones
            if any(p in col.lower() for p in ['tel', 'cel', 'fone', 'whats']):
                novos_valores = []
                for v in df[col]:
                    novo, arrumou = limpar_telefone(v)
                    if arrumou:
                        telefones_arrumados += 1
                    novos_valores.append(novo)
                df[col] = novos_valores
            # Nomes
            elif 'nome' in col.lower():
                for i, v in enumerate(df[col]):
                    if pd.notna(v):
                        original = str(v)
                        limpo = original.strip().title()
                        if original != limpo:
                            nomes_arrumados += 1
                            df.at[i, col] = limpo
            # Outros textos só tira espaço
            else:
                df[col] = df[col].astype(str).str.strip().replace('nan', '')

        # 4. Datas
        for col in df.columns:
            if 'data' in col.lower():
                antes_nulo = df[col].isna().sum()
                df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
                depois_nulo = df[col].isna().sum()
                # Se conseguiu converter, conta
                if depois_nulo < len(df):
                    datas_arrumadas += len(df) - depois_nulo

        # 5. Tirar duplicados
        antes = len(df)
        df = df.drop_duplicates()
        duplicados_removidos = antes - len(df)

        # 6. Salvar
        pasta = os.path.dirname(caminho)
        nome_novo = os.path.join(pasta, "planilha_LIMPA.xlsx")
        df.to_excel(nome_novo, index=False)

        linhas_depois = len(df)

        # 7. Montar relatório
        relatorio = f"""✅ LIMPEZA CONCLUÍDA!

📊 RESUMO:
• Linhas antes: {linhas_antes}
• Linhas depois: {linhas_depois}
• Colunas: {colunas}

🧹 O QUE FOI FEITO:
• Linhas vazias removidas: {vazias_removidas}
• Duplicados removidos: {duplicados_removidos}
• Telefones formatados: {telefones_arrumados}
• Nomes corrigidos: {nomes_arrumados}

💾 Salvo como:
planilha_LIMPA.xlsx
"""
        relatorio_label.config(text=relatorio)
        messagebox.showinfo("Pronto! ✅", "Limpeza concluída! Relatório na tela.")

    except Exception as e:
        messagebox.showerror("Erro", f"Deu erro: {e}")

tk.Button(janela, text="📂 ESCOLHER PLANILHA", command=escolher_arquivo, bg="#007AFF", fg="white", font=("Arial", 12, "bold"), height=2).pack(pady=5, padx=20, fill="x")
tk.Button(janela, text="✨ LIMPAR + GERAR RELATÓRIO", command=limpar, bg="#28a745", fg="white", font=("Arial", 12, "bold"), height=2).pack(pady=5, padx=20, fill="x")

janela.mainloop()