import sys

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QTextEdit
)

from backup_pendrive_test import fazer_backup


class BackupThread(QThread):

    log_signal = pyqtSignal(str)

    def __init__(self, origem, destino):
        super().__init__()
        self.origem = origem
        self.destino = destino

    def run(self):
        fazer_backup(
            self.origem,
            self.destino,
            log_callback=self.log_signal.emit
            )


class BackupApp(QWidget):

    def __init__(self):
        super().__init__()

        self.origem = ""
        self.destino = ""

        self.setWindowTitle("Backup para Pendrive")

        layout = QVBoxLayout()

        # label origem
        self.label_origem = QLabel(f"Pasta origem: {self.origem}")
        layout.addWidget(self.label_origem)

        btn_origem = QPushButton("Selecionar Pasta Origem")
        btn_origem.clicked.connect(self.escolher_origem)
        layout.addWidget(btn_origem)

        # label destino
        self.label_destino = QLabel(f"Pasta destino: {self.destino}")
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
        pasta = QFileDialog.getExistingDirectory(self, "Selecionar Pasta Origem")

        if pasta:
            self.origem = pasta
            self.label_origem.setText(f"Pasta origem: {pasta}")

    def escolher_destino(self):
        pasta = QFileDialog.getExistingDirectory(self, "Selecionar Pasta Destino")

        if pasta:
            self.destino = pasta
            self.label_destino.setText(f"Destino: {pasta}")

    def iniciar_backup(self):

        if not self.origem or not self.destino:
            self.log.append("Selecione origem e destino.")
            return
        
        self.thread = BackupThread(self.origem, self.destino)

        self.thread.log_signal.connect(self.log.append)

        self.thread.start()


app = QApplication(sys.argv)

janela = BackupApp()
janela.show()

sys.exit(app.exec())