import tabula # biblioteca para conversão de tabelas em pdf para DataFrames
from PyPDF2 import PdfReader # biblioteca para leitura de pdf
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

diretorio = './resultados_csv/'
os.makedirs(os.path.dirname(diretorio), exist_ok=True)


root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilenames(filetypes=(('*pdf files', '*.pdf'),))

for file in file_path:
    
    lista_tabelas = tabula.read_pdf(file, pages="all", encoding="latin-1")
    
    disciplina = []
    docente = []
    turma = []

    with open(file, 'rb') as arq:
        reader = PdfReader(arq) # não sei o que faz (implementar explicação)
        for page in reader.pages:
            texto = page.extract_text()

            # o processo de extração da turma, disciplina e docente funciona
            # utilizando o método find, que recebe uma string e retorna
            # o index da primeira ocorrência dessa string

            # caso o método não encontre a string recebemos -1 como retorno

            # o método find também pode receber um parâmetro para buscar a string
            # a partir de um index especificado

            # por fim realizamos o corte na string utilizando o index_inicial e o index_final da nossa busca

            index_inicial = texto.find("Lista de Notas e Faltas")
            if index_inicial != -1:
                # extração turma
                turma_inicio = texto.find("Turma", index_inicial)
                turma_inicio = texto.find(' ', turma_inicio) + 1
                turma_fim = texto.find(' ', turma_inicio)
                turma.append(texto[turma_inicio:turma_fim])

                # extração disciplina
                disciplina_inicio = texto.find("Disciplina", index_inicial)
                disciplina_inicio = texto.find("-", disciplina_inicio) + 2
                disciplina_fim = texto.find('\n', disciplina_inicio)
                disciplina.append(texto[disciplina_inicio:disciplina_fim])

            # extração docente
            # tive um problema quando o docente estava a definir, onde o extrator puxava
            # as informações erradas

            docente_inicio = texto.find("Docente(s)")
            if docente_inicio != -1:
                docente_inicio = texto.find(" ", docente_inicio) + 1
                turma_inicio = texto.find("Ano/Semestre", docente_inicio)
                if turma_inicio - docente_inicio > 0:
                    docente_fim = texto.find("-", docente_inicio) - 1
                    docente.append(texto[docente_inicio:docente_fim])
                else:
                    docente.append("A DEFINIR DOCENTE")
                    

    tabelas_nota = [] # nova lista para as tabelas que contém notas
    for tabela in lista_tabelas:
        if len(tabela.columns) == 12:
            tabela.drop([0, 1, 2, 3], inplace=True)
            tabela.drop(tabela.columns[0], axis=1, inplace=True)
            tabela.fillna(-1, inplace=True)
            tabela[tabela.columns[[2, 3, 4, 5, 6, 7, 8]]] = tabela[tabela.columns[[2, 3, 4, 5, 6, 7, 8]]].map(lambda x: x.replace(',','.') if isinstance(x, str) else x).astype(float)
            tabelas_nota.append(tabela)
    
    for i, tabela in enumerate(tabelas_nota):
        tabela.insert(0, 'turma', turma[i])
        tabela.insert(1, 'disciplina', disciplina[i])
        tabela.insert(2, 'docente', docente[i])
    
    tabela = pd.concat(tabelas_nota)
    tabela.columns.values[3] = "matricula"
    tabela.columns.values[4] = "nome"
    tabela.columns.values[5] = "aval_1"
    tabela.columns.values[6] = "aval_2"
    tabela.columns.values[7] = "aval_3"
    tabela.columns.values[8] = "aval_4"
    tabela.columns.values[9] = "media_parcial"
    tabela.columns.values[10] = "exame_final"
    tabela.columns.values[11] = "media_final"
    tabela.columns.values[12] = "total_faltas"
    tabela.columns.values[13] = "resultado"

    tabela.to_csv(f'./resultados_csv/{turma[i]}.csv', index=False)