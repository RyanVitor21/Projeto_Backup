import os
import shutil
import datetime


def copiar_arquivos(
    origem,
    pasta_backup,
    log_callback=None,
    progress_data=None,
    progress_callback=None,
    modo="incremental"
):

    arquivos_ignorados = ["desktop.ini", "thumbs.db"]

    nome_origem = os.path.basename(origem)
    pasta_backup = os.path.join(pasta_backup, nome_origem)

    os.makedirs(pasta_backup, exist_ok=True)

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

                copiar = False

                if modo == "snapshot":
                    copiar = True

                elif modo == "incremental":

                    if not os.path.exists(caminho_destino):
                        copiar = True

                    elif (
                        os.path.getmtime(caminho_origem)
                        > os.path.getmtime(caminho_destino)
                    ):
                        copiar = True

                if copiar:
                    shutil.copy2(caminho_origem, caminho_destino)

                    if log_callback:
                        log_callback(
                            f"[{nome_origem}] Arquivo copiado: {arquivo}"
                        )

                if progress_data:
                    progress_data["copiados"] += 1

                    if progress_callback and progress_data["total"] > 0:
                        porcentagem = int(
                            (progress_data["copiados"] / progress_data["total"]) * 100
                        )
                        progress_callback(porcentagem)

            except Exception as erro:

                if log_callback:
                    log_callback(
                        f"[{nome_origem}] Erro ao copiar {arquivo}: {erro}"
                    )

    if log_callback:
        log_callback(f"[{nome_origem}] Backup finalizado.")


def fazer_backup(
    origem,
    destino,
    modo="incremental",
    log_callback=None,
    progress_data=None,
    progress_callback=None
):

    if not os.path.exists(destino):
        if log_callback:
            log_callback("Destino não encontrado.")
        return

    if modo == "incremental":
        pasta_backup = os.path.join(destino, "backup", "incremental")

    else:
        data_atual = datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
        pasta_backup = os.path.join(destino, "backup", "snapshots", data_atual)

    copiar_arquivos(
        origem,
        pasta_backup,
        log_callback,
        progress_data,
        progress_callback,
        modo
    )


def contar_arquivos(origem):

    arquivos_ignorados = ["desktop.ini", "thumbs.db"]
    total = 0

    for root, dirs, files in os.walk(origem):
        for arquivo in files:
            if arquivo.lower() not in arquivos_ignorados:
                total += 1

    return total