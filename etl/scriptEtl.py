###### ajustes necessários
# disciplinas com dois professores (educação física)
# matrícula docente concatenada com docente (VANILDA I2021TF)
# nomes longos ocupam 3 linhas (I2081TF)
#I2042ME e I2122ME lendo a tabela de faltas como tabela de notas

import tabula # biblioteca para conversão de tabelas em pdf para DataFrames
from PyPDF2 import PdfReader # biblioteca para leitura de pdf
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import os

diretorio = './resultados_csv/'
os.makedirs(os.path.dirname(diretorio), exist_ok=True)


root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilenames(filetypes=(('*pdf files', '*.pdf'),))

script_start = datetime.now()

for file in file_path:
    file_start = datetime.now()

    print(f"Extraindo arquivo: {file}")
    lista_tabelas = tabula.read_pdf(file, pages="all", encoding="latin-1")
    
    disciplina = []
    codigo_disciplina = []
    docente = []
    matricula_docente = []
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
            
            index_inicial = texto.find("Diário de Turma")
            if index_inicial != -1:
                # extração código disciplina
                codigo_disciplina_inicio = texto.find("Código", index_inicial)
                codigo_disciplina_inicio = texto.find(" ", codigo_disciplina_inicio) + 1
                codigo_disciplina_fim = texto.find("\n", codigo_disciplina_inicio)
                codigo_disciplina.append(texto[codigo_disciplina_inicio:codigo_disciplina_fim])
                docente_inicio = texto.find("Docente(s)")
                if docente_inicio != -1:
                    matricula_docente_inicio = texto.find("\n", docente_inicio) + 1
                    docente_inicio = texto.find(" ", docente_inicio) + 1
                    matricula_docente_fim = texto.find(" ", matricula_docente_inicio)
                    turma_inicio = texto.find("Ano/Semestre", docente_inicio)

                    matricula_docente_atual = texto[matricula_docente_inicio:matricula_docente_fim]
                    if turma_inicio - docente_inicio > 0 and matricula_docente_atual.isnumeric():
                        docente_fim = texto.find("-", docente_inicio) - 1
                        docente.append(texto[docente_inicio:docente_fim])
                        matricula_docente.append(matricula_docente_atual)
                    elif turma_inicio - docente_inicio  > 0 and not matricula_docente_atual.isnumeric():
                        nova_matricula_docente_atual = ""
                        novo_docente_atual = ""
                        for letra in matricula_docente_atual:
                            if letra.isdigit():
                                nova_matricula_docente_atual += letra
                            else:
                                novo_docente_atual += letra
                        matricula_docente.append(nova_matricula_docente_atual)
                        docente_fim  = texto.find("-", docente_inicio) - 1
                        docente.append(novo_docente_atual + " " + texto[docente_inicio:docente_fim])
                    else:
                        docente.append("A DEFINIR DOCENTE")
                        matricula_docente.append(-1.0)

            # extração docente
            # tive um problema quando o docente estava a definir, onde o extrator puxava
            # as informações erradas
            # isso pode ser corrigido indentificando se a string "docente" é maior que 0

            
                    
    tabelas_nota = [] # nova lista para as tabelas que contém notas
    for tabela in lista_tabelas:
        if len(tabela.columns) == 12:
            tabela.drop([0, 1, 2, 3], inplace=True)
            tabela.drop(tabela.columns[0], axis=1, inplace=True)
            tabela.fillna("-1.0", inplace=True)
            tabela[tabela.columns[8]] = tabela[tabela.columns[8]].apply(lambda x: x.replace('.', ',') if isinstance(x, str) else x.str.replace('.', ','))
            tabela[tabela.columns[9]] = tabela[tabela.columns[9]].apply(lambda x: x.int if x != -1.0 and isinstance(x, int) else x)
            #tabela[tabela.columns[[2, 3, 4, 5, 6, 7, 8]]] = tabela[tabela.columns[[2, 3, 4, 5, 6, 7, 8]]].map(lambda x: x.replace(',','.') if isinstance(x, str) else x).astype(float)
            tabelas_nota.append(tabela)
    
    for i, tabela in enumerate(tabelas_nota):
        tabela.insert(0, 'turma', turma[i])
        tabela.insert(1, 'disciplina', disciplina[i])
        tabela.insert(1, 'codigo_disciplina', codigo_disciplina[i])
        tabela.insert(1, 'docente', docente[i])
        tabela.insert(1, 'matricula_docente', matricula_docente[i])
    
    tabela = pd.concat(tabelas_nota)
    tabela.columns.values[5] = "matricula"
    tabela.columns.values[6] = "nome"
    tabela.columns.values[7] = "aval_1"
    tabela.columns.values[8] = "aval_2"
    tabela.columns.values[9] = "aval_3"
    tabela.columns.values[10] = "aval_4"
    tabela.columns.values[11] = "media_parcial"
    tabela.columns.values[12] = "exame_final"
    tabela.columns.values[13] = "media_final"
    tabela.columns.values[14] = "total_faltas"
    tabela.columns.values[15] = "resultado"
    
    tabela.to_csv(f"./resultados_csv/{turma[i]}.csv", index=False)
    print(f"Concluído. ({datetime.now()- file_start})")

print("PDFs concluídos.")
tempo_total = datetime.now() - script_start
print(f"Tempo de execução total: {tempo_total}")
print(f"Tempo médio por arquivo: {tempo_total / len(file_path)}")