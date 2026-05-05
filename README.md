# 📦 Sistema de Backup de Arquivos em Python

Projeto desenvolvido em **Python + PyQt5** para realizar **backup de arquivos e pastas** com interface gráfica, suporte a backup incremental, snapshots completos e backup automático.

O objetivo do sistema é facilitar a proteção de dados importantes em dispositivos externos como pendrive ou HD externo.

---

# 🚀 Início rápido

## 1. Clonar o projeto

```bash
git clone URL_DO_REPOSITORIO
```

---

## 2. Entrar na pasta do projeto

```bash
cd python-projeto-backup
```

---

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 4. Rodar o projeto

```bash
python interface.py
```

ou:

```bash
py interface.py
```

---

# 🔄 Fluxo completo para colaboradores

```bash
git clone URL_DO_REPOSITORIO
cd python-projeto-backup
pip install -r requirements.txt
python interface.py
```

---

# 🛠 Comandos úteis

## Formatar código com Black

```bash
black .
```

ou:

```bash
black interface.py
```

---

## Gerar executável

```bash
pyinstaller --onefile --windowed interface.py
```

Executável gerado em:

```text
dist/
```

---

# 🚀 Funcionalidades

* 📁 Backup de múltiplas pastas
* 🔄 Backup incremental
* 📸 Snapshot completo
* ⏱ Backup automático a cada 10 minutos
* 📊 Barra de progresso
* 📝 Logs em tempo real
* 🗂 Organização automática dos backups
* 🖥 Interface gráfica intuitiva

---

# 📂 Estrutura do projeto

```text
python-projeto-backup/
│── interface.py
│── backup_incremental_snapshot.py
│── requirements.txt
│── README.md
│── .gitignore
```

---

# 📌 Observações

* O backup automático funciona apenas enquanto o programa estiver aberto.
* O backup incremental copia apenas arquivos novos ou alterados.
* O snapshot cria uma cópia completa separada por data e hora.

---

# 📄 Licença

Projeto livre para estudo, melhorias e colaboração.


# 🧱 Como gerar o executável (.exe)

Siga exatamente esta ordem:

## 1. Instalar o PyInstaller (caso não esteja instalado)

```bash
pip install pyinstaller
```

---

## 2. Gerar o executável

```bash
pyinstaller --onefile --windowed interface.py
```

Se quiser definir um ícone:

```bash
pyinstaller --onefile --windowed --icon=icone.ico interface.py
```

---

## 3. Localizar o executável

Após finalizar, o arquivo estará em:

```text
dist/interface.exe
```

---

## 📦 Para compartilhar

Compacte o `.exe` em `.zip` antes de enviar:

```text
interface.exe → interface.zip
```

Assim evita problemas de envio e facilita o download.
