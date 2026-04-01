import sys

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QTextEdit, QProgressBar
)

from backup_pendrive_test import fazer_backup, contar_arquivos


class BackupThread(QThread):

    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)

    def __init__(self, origens, destino):
        super().__init__()
        self.origens = origens
        self.destino = destino

    def run(self):

        total = 0
        for origem in self.origens:
            total += contar_arquivos(origem)

        progresso = {"copiados": 0, "total": total}

        for origem in self.origens:
            fazer_backup(
                origem,
                self.destino,
                log_callback=self.log_signal.emit,
                progress_data=progresso,
                progress_callback=self.progress_signal.emit
            )

        # 🔥 garante 100% no final
        self.progress_signal.emit(100)


class BackupApp(QWidget):

    def __init__(self):
        super().__init__()

        self.origens = []
        self.destino = ""

        self.setWindowTitle("Backup para Pendrive")

        layout = QVBoxLayout()

        # barra de progresso
        self.progress = QProgressBar()
        self.progress.setFormat("Progresso: %p%")
        layout.addWidget(self.progress)

        # label origem
        self.label_origem = QLabel("Pastas origem: nenhuma selecionada")
        layout.addWidget(self.label_origem)

        btn_origem = QPushButton("Adicionar Pasta Origem")
        btn_origem.clicked.connect(self.escolher_origem)
        layout.addWidget(btn_origem)

        btn_limpar = QPushButton("Limpar Pastas")
        btn_limpar.clicked.connect(self.limpar_origens)
        layout.addWidget(btn_limpar)

        # label destino
        self.label_destino = QLabel("Pasta destino: não selecionada")
        layout.addWidget(self.label_destino)

        btn_destino = QPushButton("Selecionar Pasta Destino")
        btn_destino.clicked.connect(self.escolher_destino)
        layout.addWidget(btn_destino)

        # botão backup
        btn_backup = QPushButton("Iniciar Backup")
        btn_backup.clicked.connect(self.iniciar_backup)
        layout.addWidget(btn_backup)

        # log
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
        pasta = QFileDialog.getExistingDirectory(self, "Selecionar Pasta Destino")

        if pasta:
            self.destino = pasta
            self.label_destino.setText(f"Destino: {pasta}")

    def iniciar_backup(self):

        if not self.origens or not self.destino:
            self.log.append("Selecione pelo menos uma origem e um destino.")
            return

        self.progress.setValue(0)

        self.thread = BackupThread(self.origens, self.destino)

        self.thread.log_signal.connect(self.log.append)
        self.thread.progress_signal.connect(self.progress.setValue)

        self.thread.start()


app = QApplication(sys.argv)

janela = BackupApp()
janela.show()

sys.exit(app.exec())