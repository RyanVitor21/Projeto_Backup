import os
import shutil
import datetime


def fazer_backup(origem, destino, log_callback=None):

    if not os.path.exists(destino):
        if log_callback:
            log_callback("Destino não encontrado.")
        return

    data_atual = datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S")

    pasta_backup = os.path.join(destino, "backup", data_atual)

    os.makedirs(pasta_backup, exist_ok=True)

    arquivos_ignorados = ["desktop.ini", "thumbs.db"]

    for root, dirs, files in os.walk(origem):

        # criar estrutura da pasta no backup
        caminho_relativo = os.path.relpath(root, origem)
        pasta_destino = os.path.join(pasta_backup, caminho_relativo)

        os.makedirs(pasta_destino, exist_ok=True)

        for arquivo in files:

            if arquivo.lower() in arquivos_ignorados:
                continue

            caminho_origem = os.path.join(root, arquivo)
            caminho_destino = os.path.join(pasta_destino, arquivo)

            try:

                shutil.copy2(caminho_origem, caminho_destino)

                if log_callback:
                    log_callback(f"Arquivo copiado: {arquivo}")

            except Exception as erro:

                if log_callback:
                    log_callback(f"Erro ao copiar {arquivo}: {erro}")

    if log_callback:
        log_callback("Backup finalizado.")