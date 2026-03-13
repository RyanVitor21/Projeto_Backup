import os
import shutil
import datetime

origem = r"C:\Users\Ryan\Music"
pendrive = r"E:\\"

# verificar se o pendrive está conectado
if not os.path.exists(pendrive):
    print("Pendrive não conectado.")
    exit()

data_atual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

pasta_backup = os.path.join(pendrive, "backup", data_atual)

os.makedirs(pasta_backup, exist_ok=True)

arquivo_log = os.path.join(pasta_backup, "log_backup.txt")

arquivos_ignorados = ["desktop.ini", "thumbs.db"]

lista_arquivos = os.walk(origem)

with open(arquivo_log, "a", encoding="utf-8") as log:

    log.write(f"\nBackup iniciado: {data_atual}\n")

    for arquivo in lista_arquivos:

        if arquivo.lower() in arquivos_ignorados:
            continue

        caminho_origem = os.path.join(origem, arquivo)
        caminho_destino = os.path.join(pasta_backup, arquivo)

        try:

            # evitar duplicação
            if os.path.exists(caminho_destino):
                log.write(f"Arquivo já existe: {arquivo}\n")
                continue

            if os.path.isfile(caminho_origem):

                shutil.copy2(caminho_origem, caminho_destino)

                log.write(f"Arquivo copiado: {arquivo}\n")

            elif os.path.isdir(caminho_origem):

                shutil.copytree(caminho_origem, caminho_destino)

                log.write(f"Pasta copiada: {arquivo}\n")

        except Exception as erro:

            log.write(f"Erro ao copiar {arquivo}: {erro}\n")

    log.write("Backup finalizado.\n")

print("Backup concluído com sucesso.")