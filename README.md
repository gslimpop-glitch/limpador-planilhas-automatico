# 🧹 Limpador de Planilhas Automático

Ferramenta em Python para limpar e padronizar planilhas Excel sujas antes de subir para o banco de dados ou sistema.

## O que ele faz
- ✅ Remove linhas vazias
- ✅ Remove duplicados
- ✅ Padroniza telefones para (11) 99999-9999
- ✅ Corrige nomes (tira espaço, deixa Title Case)
- ✅ Padroniza datas
- ✅ Gera relatório de limpeza
- ✅ Cria arquivo novo sem apagar o original

## Tecnologias
Python | Pandas | Tkinter

## Resultado real em teste
Base com 73 linhas:
- 12 linhas vazias removidas
- 2 duplicados removidos
- 40 telefones formatados
- 56 nomes corrigidos
- Tempo: ~2 segundos

## Como usar
1. Rode `python limpador.py`
2. Clique em ESCOLHER PLANILHA
3. Clique em LIMPAR + GERAR RELATÓRIO
4. Arquivo limpo salvo como `planilha_LIMPA.xlsx`

Feito por Gabriel Ribeiro
