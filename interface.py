import sys

from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QTextEdit, QProgressBar
)

from backup_incremental_snapshot import fazer_backup, contar_arquivos


class BackupThread(QThread):

    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)

    def __init__(self, origens, destino, modo):
        super().__init__()
        self.origens = origens
        self.destino = destino
        self.modo = modo

    def run(self):

        total = 0
        for origem in self.origens:
            total += contar_arquivos(origem)

        progresso = {"copiados": 0, "total": total}

        for origem in self.origens:
            fazer_backup(
                origem,
                self.destino,
                modo=self.modo,
                log_callback=self.log_signal.emit,
                progress_data=progresso,
                progress_callback=self.progress_signal.emit
            )

        self.progress_signal.emit(100)


class BackupApp(QWidget):

    def __init__(self):
        super().__init__()

        self.origens = []
        self.destino = ""
        self.thread = None

        # timer automático (10 minutos)
        self.timer = QTimer()
        self.timer.timeout.connect(self.backup_automatico)

        self.setWindowTitle("Sistema de Backup")

        layout = QVBoxLayout()

        self.progress = QProgressBar()
        self.progress.setFormat("Progresso: %p%")
        layout.addWidget(self.progress)

        self.label_origem = QLabel("Pastas origem: nenhuma selecionada")
        layout.addWidget(self.label_origem)

        btn_origem = QPushButton("Adicionar Pasta Origem")
        btn_origem.clicked.connect(self.escolher_origem)
        layout.addWidget(btn_origem)

        btn_limpar = QPushButton("Limpar Pastas")
        btn_limpar.clicked.connect(self.limpar_origens)
        layout.addWidget(btn_limpar)

        self.label_destino = QLabel("Pasta destino: não selecionada")
        layout.addWidget(self.label_destino)

        btn_destino = QPushButton("Selecionar Pasta Destino")
        btn_destino.clicked.connect(self.escolher_destino)
        layout.addWidget(btn_destino)

        btn_incremental = QPushButton("Backup Rápido (Incremental)")
        btn_incremental.clicked.connect(
            lambda: self.iniciar_backup("incremental")
        )
        layout.addWidget(btn_incremental)

        btn_snapshot = QPushButton("Criar Snapshot Completo")
        btn_snapshot.clicked.connect(
            lambda: self.iniciar_backup("snapshot")
        )
        layout.addWidget(btn_snapshot)

        # botão ativar automático
        btn_auto_on = QPushButton("Ativar Backup Automático (10 min)")
        btn_auto_on.clicked.connect(self.ativar_backup_automatico)
        layout.addWidget(btn_auto_on)

        # botão parar automático
        btn_auto_off = QPushButton("Parar Backup Automático")
        btn_auto_off.clicked.connect(self.parar_backup_automatico)
        layout.addWidget(btn_auto_off)

        self.log = QTextEdit()
        layout.addWidget(self.log)

        self.setLayout(layout)

    def escolher_origem(self):
        pasta = QFileDialog.getExistingDirectory(self, "Selecionar Pasta")

        if pasta:
            self.origens.append(pasta)

            self.label_origem.setText(
                "Pastas:\n" + "\n".join(self.origens)
            )

    def limpar_origens(self):
        self.origens = []
        self.label_origem.setText("Pastas origem: nenhuma selecionada")

    def escolher_destino(self):
        pasta = QFileDialog.getExistingDirectory(
            self,
            "Selecionar Pasta Destino"
        )

        if pasta:
            self.destino = pasta
            self.label_destino.setText(f"Destino: {pasta}")

    def iniciar_backup(self, modo):

        if not self.origens or not self.destino:
            self.log.append(
                "Selecione pelo menos uma origem e um destino."
            )
            return

        # evita iniciar outro backup enquanto um está rodando
        if self.thread and self.thread.isRunning():
            self.log.append("Backup já está em andamento.")
            return

        self.progress.setValue(0)

        self.thread = BackupThread(
            self.origens,
            self.destino,
            modo
        )

        self.thread.log_signal.connect(self.log.append)
        self.thread.progress_signal.connect(self.progress.setValue)

        self.thread.start()

    def ativar_backup_automatico(self):

        if not self.origens or not self.destino:
            self.log.append(
                "Selecione origem e destino antes de ativar."
            )
            return

        self.timer.start(120000)  # 10 minutos
        self.log.append("Backup automático ativado.")

    def parar_backup_automatico(self):

        self.timer.stop()
        self.log.append("Backup automático parado.")

    def backup_automatico(self):

        self.log.append("Iniciando backup automático...")
        self.iniciar_backup("incremental")


app = QApplication(sys.argv)

janela = BackupApp()
janela.show()

sys.exit(app.exec())