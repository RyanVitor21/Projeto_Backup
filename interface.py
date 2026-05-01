import sys

from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QTextEdit, QProgressBar,
    QListWidget, QMessageBox, QGroupBox
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
        self.timer = QTimer()

        self.setWindowTitle("Sistema de Backup")
        self.resize(550, 700)

        self.setStyleSheet("""
    QPushButton {
        padding: 8px;
        border-radius: 6px;
        border: 2px solid black;   
    }

    QProgressBar {
        height: 20px;
    }

    QTextEdit {
        border: 1px solid gray;
    }

    QGroupBox {
        font-weight: bold;
        margin-top: 10px;
        padding-top: 15px;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
                        
    }
""")
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # =========================
        # PROGRESSO
        # =========================
        grupo_progresso = QGroupBox("Progresso")
        progresso_layout = QVBoxLayout()

        self.progress = QProgressBar()
        self.progress.setFormat("Progresso: %p%")
        progresso_layout.addWidget(self.progress)

        grupo_progresso.setLayout(progresso_layout)
        layout.addWidget(grupo_progresso)

        # =========================
        # ORIGENS
        # =========================
        grupo_origens = QGroupBox("Pastas de Origem")
        origens_layout = QVBoxLayout()

        self.lista_origens = QListWidget()
        origens_layout.addWidget(self.lista_origens)

        btn_origem = QPushButton("Adicionar Pasta")
        btn_origem.clicked.connect(self.escolher_origem)
        origens_layout.addWidget(btn_origem)

        btn_remover = QPushButton("Remover Pasta Selecionada")
        btn_remover.clicked.connect(self.remover_origem)
        origens_layout.addWidget(btn_remover)

        btn_limpar = QPushButton("Limpar Todas")
        btn_limpar.clicked.connect(self.limpar_origens)
        origens_layout.addWidget(btn_limpar)

        grupo_origens.setLayout(origens_layout)
        layout.addWidget(grupo_origens)

        # =========================
        # DESTINO
        # =========================
        grupo_destino = QGroupBox("Destino do Backup")
        destino_layout = QVBoxLayout()

        self.label_destino = QLabel("Nenhum destino selecionado")
        destino_layout.addWidget(self.label_destino)

        btn_destino = QPushButton("Selecionar Destino")
        btn_destino.clicked.connect(self.escolher_destino)
        destino_layout.addWidget(btn_destino)

        grupo_destino.setLayout(destino_layout)
        layout.addWidget(grupo_destino)

        # =========================
        # OPERAÇÕES
        # =========================
        grupo_operacoes = QGroupBox("Operações")
        operacoes_layout = QVBoxLayout()

        btn_incremental = QPushButton("Atualizar Backup(backup incremental:)")
        btn_incremental.clicked.connect(
            lambda: self.iniciar_backup("incremental")
        )
        operacoes_layout.addWidget(btn_incremental)

        btn_snapshot = QPushButton("Criar Backup Completo")
        btn_snapshot.clicked.connect(
            lambda: self.iniciar_backup("snapshot")
        )
        operacoes_layout.addWidget(btn_snapshot)

        btn_auto = QPushButton("Ativar Backup Automático (10 min)")
        btn_auto.clicked.connect(self.ativar_backup_automatico)
        operacoes_layout.addWidget(btn_auto)

        btn_parar_auto = QPushButton("Parar Backup Automático")
        btn_parar_auto.clicked.connect(self.parar_backup_automatico)
        operacoes_layout.addWidget(btn_parar_auto)

        grupo_operacoes.setLayout(operacoes_layout)
        layout.addWidget(grupo_operacoes)

        # =========================
        # STATUS
        # =========================
        self.status_label = QLabel("Status: Pronto")
        layout.addWidget(self.status_label)

        # =========================
        # LOGS
        # =========================
        grupo_logs = QGroupBox("Logs")
        logs_layout = QVBoxLayout()

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        logs_layout.addWidget(self.log)

        grupo_logs.setLayout(logs_layout)
        layout.addWidget(grupo_logs)

        self.setLayout(layout)

    def escolher_origem(self):
        pasta = QFileDialog.getExistingDirectory(
            self,
            "Selecionar Pasta"
        )

        if pasta:
            if pasta not in self.origens:
                self.origens.append(pasta)
                self.lista_origens.addItem(pasta)

    def remover_origem(self):
        item = self.lista_origens.currentItem()

        if item:
            pasta = item.text()
            self.origens.remove(pasta)
            self.lista_origens.takeItem(
                self.lista_origens.row(item)
            )

    def limpar_origens(self):

        resposta = QMessageBox.question(
            self,
            "Confirmar",
            "Deseja remover todas as pastas?"
        )

        if resposta == QMessageBox.Yes:
            self.origens = []
            self.lista_origens.clear()

    def escolher_destino(self):
        pasta = QFileDialog.getExistingDirectory(
            self,
            "Selecionar Destino"
        )

        if pasta:
            self.destino = pasta
            self.label_destino.setText(pasta)

    def iniciar_backup(self, modo):

        if not self.origens or not self.destino:
            self.log.append(
                "Selecione pelo menos uma origem e um destino."
            )
            return

        self.progress.setValue(0)
        self.status_label.setText("Status: Executando backup...")

        self.thread = BackupThread(
            self.origens,
            self.destino,
            modo
        )

        self.thread.log_signal.connect(self.log.append)
        self.thread.progress_signal.connect(
            self.progress.setValue
        )

        self.thread.finished.connect(
            lambda: self.status_label.setText(
                "Status: Backup concluído"
            )
        )

        self.thread.start()

    def ativar_backup_automatico(self):

        self.timer.timeout.connect(
            lambda: self.iniciar_backup("incremental")
        )

        self.timer.start(600000)

        self.log.append("Backup automático ativado.")
        self.status_label.setText(
            "Status: Backup automático ativo"
        )

    def parar_backup_automatico(self):

        self.timer.stop()

        self.log.append("Backup automático parado.")
        self.status_label.setText(
            "Status: Automático desativado"
        )


app = QApplication(sys.argv)

janela = BackupApp()
janela.show()

sys.exit(app.exec())