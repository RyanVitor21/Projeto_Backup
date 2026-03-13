# Janela para selecionar a pasta do nosso computador
import os
from tkinter.filedialog import askdirectory
import shutil
import datetime

nome_pasta_selecionada = askdirectory()
print(nome_pasta_selecionada)

lista_arquivos = os.listdir(nome_pasta_selecionada)
print(lista_arquivos)

# fazer o backup dos arquivos que estão nessa pasta  
nome_pasta_backup = "backup"
nome_completo_pasta_backup = f"{nome_pasta_selecionada}/{nome_pasta_backup}"
if not os.path.exists(nome_completo_pasta_backup):
    os.mkdir(nome_completo_pasta_backup)

data_atual = datetime.datetime.today().strftime("%Y-%m-%d %H-%M-%S")
print(data_atual)

for arquivo in lista_arquivos:
    print(arquivo)
    nome_completo_arquivo = f"{nome_pasta_selecionada}/{arquivo}"
    nome_final_arquivo = f"{nome_completo_pasta_backup}/{data_atual}/{arquivo}"


    if not os.path.exists(f"{nome_completo_pasta_backup}/{data_atual}"):
        os.makedirs(f"{nome_completo_pasta_backup}/{data_atual}")
        
    if "." in arquivo:
        shutil.copy2(nome_completo_arquivo, nome_final_arquivo)
    elif  "backup" != arquivo:
        shutil.copytree(nome_completo_arquivo, nome_final_arquivo)

    