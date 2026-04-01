import os
import shutil
import datetime


def fazer_backup(origem, destino, log_callback=None, progress_data=None, progress_callback=None):

    if not os.path.exists(destino):
        if log_callback:
            log_callback("Destino não encontrado.")
        return

    data_atual = datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S")

    nome_origem = os.path.basename(origem)

    pasta_backup = os.path.join(destino, "backup", data_atual, nome_origem)

    os.makedirs(pasta_backup, exist_ok=True)

    arquivos_ignorados = ["desktop.ini", "thumbs.db"]

    for root, dirs, files in os.walk(origem):

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

                # 🔥 progresso corrigido
                if progress_data:
                    progress_data["copiados"] += 1

                    if progress_callback and progress_data["total"] > 0:
                        porcentagem = int(
                            (progress_data["copiados"] / progress_data["total"]) * 100
                        )
                        progress_callback(porcentagem)

                if log_callback:
                    log_callback(f"[{nome_origem}] Arquivo copiado: {arquivo}")

            except Exception as erro:
                if log_callback:
                    log_callback(f"[{nome_origem}] Erro ao copiar {arquivo}: {erro}")

    if log_callback:
        log_callback(f"[{nome_origem}] Backup finalizado.")


def contar_arquivos(origem):

    arquivos_ignorados = ["desktop.ini", "thumbs.db"]
    total = 0

    for root, dirs, files in os.walk(origem):
        for arquivo in files:
            if arquivo.lower() not in arquivos_ignorados:
                total += 1

    return total