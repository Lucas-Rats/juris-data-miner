# JURIS-DATA-MINER
# Proibida a modificação ou uso comercial sem autorização expressa.
# Proibida reprodução, distribuição ou engenharia reversa sem autorização.
# Copyright © 2025 Lucas Rats. Todos os direitos reservados.

from pathlib import Path
import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QPushButton, 
                            QLabel, QFileDialog, QTextEdit, QProgressBar,
                            QGroupBox, QHBoxLayout, QComboBox, QListWidget,
                            QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configurações do projeto
        self.BASE_DIR = Path(__file__).parent.parent.parent
        self.arquivos_selecionados = []
        
        # Configurações da janela
        self.setWindowTitle("Minerador de Jurisprudências v2.0")
        self.setMinimumSize(QSize(800, 600))
        
        # Inicializa a interface
        self.setup_ui()

    def setup_ui(self):
        """Configura todos os componentes da interface."""
        # Widget Central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout Principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 1. Grupo de Upload
        upload_group = QGroupBox("Seleção de Documentos")
        upload_layout = QVBoxLayout()
        
        self.btn_load = QPushButton("Carregar Petições")
        self.btn_load.setIcon(QIcon.fromTheme('document-open'))
        self.btn_load.clicked.connect(self.load_files)

        self.btn_remove = QPushButton("Remover Selecionados")
        self.btn_remove.setIcon(QIcon.fromTheme('list-remove'))
        self.btn_remove.setEnabled(False)
        self.btn_remove.clicked.connect(self._remove_files)
        
        self.label_files = QLabel("Nenhum arquivo selecionado")
        self.label_files.setAlignment(Qt.AlignCenter)
        
        self.file_list = QListWidget()
        
        upload_layout.addWidget(self.btn_load)
        upload_layout.addWidget(self.btn_remove)
        upload_layout.addWidget(self.label_files)
        upload_layout.addWidget(self.file_list)
        upload_group.setLayout(upload_layout)
        
        # 2. Grupo de Visualização
        preview_group = QGroupBox("Pré-visualização")
        self.text_preview = QTextEdit()
        self.text_preview.setReadOnly(True)
        self.text_preview.setPlaceholderText("O conteúdo do documento aparecerá aqui...")
        
        preview_layout = QVBoxLayout()
        preview_layout.addWidget(self.text_preview)
        preview_group.setLayout(preview_layout)
        
        # 3. Grupo de Ações
        action_group = QGroupBox("Ações")
        self.btn_process = QPushButton("Processar Documentos")
        self.btn_process.setEnabled(False)
        
        self.combo_format = QComboBox()
        self.combo_format.addItems(["PDF", "CSV", "Markdown"])
        
        self.btn_export = QPushButton("Exportar Resultados")
        self.btn_export.setEnabled(False)
        
        action_layout = QHBoxLayout()
        action_layout.addWidget(self.btn_process)
        action_layout.addWidget(self.combo_format)
        action_layout.addWidget(self.btn_export)
        action_group.setLayout(action_layout)
        
        # 4. Barra de Progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        
        # Adiciona todos ao layout principal
        main_layout.addWidget(upload_group)
        main_layout.addWidget(preview_group)
        main_layout.addWidget(action_group)
        main_layout.addWidget(self.progress_bar)
        
        # Conecta sinais
        self.btn_process.clicked.connect(self.processar_arquivos)
        self.file_list.itemSelectionChanged.connect(self._update_status)
        self.file_list.itemSelectionChanged.connect(self._show_file_preview)

    def load_files(self):
        """Abre diálogo para seleção de arquivos."""
        default_path = str(self.BASE_DIR / "data/input")
        os.makedirs(default_path, exist_ok=True)
        
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecionar Petições",
            default_path,
            "Documentos (*.pdf *.docx *.txt)"
        )
        
        if files:
            self.arquivos_selecionados = []
            self.file_list.clear()
            
            for file in files:
                if file.lower().endswith(('.pdf', '.docx', '.txt')):
                    self.arquivos_selecionados.append(file)
                    self.file_list.addItem(os.path.basename(file))
            
            self._update_status()

    def _remove_files(self):
        """Remove arquivos selecionados da lista."""
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            return
    
        # Confirmação antes de remover
        reply = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            f"Remover {len(selected_items)} arquivo(s) selecionado(s)?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            for item in selected_items:
                index = self.file_list.row(item)
                self.arquivos_selecionados.pop(index)
                self.file_list.takeItem(index)
            
            self._update_status()

    def _update_status(self):
        """Atualiza o status da interface."""
        count = len(self.arquivos_selecionados)
        self.label_files.setText(f"{count} arquivo(s) selecionado(s)")
        self.btn_process.setEnabled(count > 0)
        self.btn_remove.setEnabled(count > 0 and len(self.file_list.selectedItems()) > 0)

    def _show_file_preview(self):
        """Mostra pré-visualização do arquivo selecionado na lista."""
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            return
            
        file_index = self.file_list.row(selected_items[0])
        file_path = self.arquivos_selecionados[file_index]
        
        # Simulação - substituir pela leitura real depois
        self.text_preview.setText(f"Pré-visualização de: {os.path.basename(file_path)}\n\n"
                                "Esta funcionalidade mostrará o conteúdo extraído do documento.")

    def processar_arquivos(self):
        """Processa os arquivos selecionados."""
        if not self.arquivos_selecionados:
            return
            
        self.progress_bar.show()
        self.progress_bar.setRange(0, len(self.arquivos_selecionados))
        
        for i, file_path in enumerate(self.arquivos_selecionados, 1):
            self.progress_bar.setValue(i)
            QApplication.processEvents()
            
            # TODO: Implementar processamento real aqui
            print(f"Processando: {file_path}")
        
        self.progress_bar.hide()
        self.btn_export.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    
    # Configura estilo visual
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()