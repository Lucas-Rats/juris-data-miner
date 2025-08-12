#JURIS-DATA-MINER
#Proibida a modificação ou uso comercial sem autorização expressa.
#Proibida reprodução, distribuição ou engenharia reversa sem autorização.
#Copyright © 2025 Lucas Rats. Todos os direitos reservados.

# Importando Bibliotecas
from pathlib import Path  # Biblioteca para manipular caminhos de arquivos multiplataformas
import os  # Biblioteca para operações com sistemas de arquivos
from PyQt5.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, 
                            QWidget, QListWidget, QLabel, QPushButton,
                            QFileDialog)  # Biblioteca de componentes da interface gráfica
import sys  # Biblioteca para interação com o sistema

class MainWindow(QMainWindow):
    
    # Inicializa a janela principal do aplicativo. Configura propriedades básicas e inicializa a interface.
    def __init__(self):

        super().__init__()  # Chama o construtor da classe pai (QMainWindow)
        
        # Define o caminho base do projeto (3 níveis acima do arquivo atual)
        self.BASE_DIR = Path(__file__).parent.parent.parent
        
        # Configurações iniciais da janela:
        self.setWindowTitle("Minerador de Jurisprudências")  # Título da janela
        self.setGeometry(100, 100, 800, 606)  # Posição (x,y) e tamanho (largura, altura)

        # Lista para armazenar os caminhos completos dos arquivos selecionados
        self.arquivos_selecionados = []
        
        # Chama o método que constrói a interface
        self.setup_ui()

    # Constroi todos os componentes da interface gráfica
    def setup_ui(self):
        
        # Widget Central - container principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)  # Define como widget central

        # Layout Principal - organiza os componentes verticalmente
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        # Botão para carregar arquivos
        self.btn_load = QPushButton("Carregar Petições")
        self.btn_load.clicked.connect(self.load_files)  # Conecta o clique ao método
        self.layout.addWidget(self.btn_load)  # Adiciona ao layout

        # Rótulo para a lista de arquivos
        self.label_files = QLabel("Arquivos selecionados:")
        self.layout.addWidget(self.label_files)

        # Lista para exibir os nomes dos arquivos selecionados
        self.file_list = QListWidget()
        self.layout.addWidget(self.file_list)

        # Botão para processar os arquivos
        self.btn_process = QPushButton("Processar")
        self.btn_process.setEnabled(False)  # Inicia desabilitado
        self.btn_process.clicked.connect(self.processar_arquivos)  # Conecta ao método
        self.layout.addWidget(self.btn_process)

    # Abre diálogo para seleção de arquivos PDF/DOCX. Armazena os arquivos válidos e atualiza a interface.
    def load_files(self):

        # Define o caminho padrão como data/input dentro do projeto
        default_path = str(self.BASE_DIR / "data/input")
        
        # Cria o diretório se não existir
        if not os.path.exists(default_path):
            os.makedirs(default_path)  # Cria todos os diretórios necessários
        
        # Abre o diálogo de seleção de arquivos
        files, _ = QFileDialog.getOpenFileNames(
            self,  # Janela pai
            "Selecionar Petições",  # Título do diálogo
            default_path,  # Diretório inicial
            "Documentos (*.pdf *.docx)"  # Filtro de extensões
        )
        
        if files:  # Se arquivos foram selecionados
            self.arquivos_selecionados = []  # Limpa lista anterior
            self.file_list.clear()  # Limpa a exibição
            
            for file in files:
                # Verifica se a extensão é .pdf ou .docx (case insensitive)
                if file.lower().endswith(('.pdf', '.docx')):
                    self.arquivos_selecionados.append(file)  # Armazena caminho completo
                    self.file_list.addItem(os.path.basename(file))  # Mostra apenas o nome
            
            # Habilita o botão de processar se há arquivos válidos
            self.btn_process.setEnabled(len(self.arquivos_selecionados) > 0)

    # Método que será chamado para processar os arquivos selecionados. Atualmente apenas exibe os caminhos no terminal.
    def processar_arquivos(self):
        
        if not self.arquivos_selecionados:  # Se não há arquivos
            return  # Sai da função
            
        # Exibe os arquivos que serão processados
        print(f"Arquivos para processar: {self.arquivos_selecionados}")

# Função principal que inicia a aplicação.
def main():
    
    app = QApplication(sys.argv)  # Cria a aplicação Qt
    window = MainWindow()  # Cria a janela principal
    window.show()  # Mostra a janela
    sys.exit(app.exec_())  # Inicia o loop de eventos e trata encerramento

# Ponto de entrada do programa - só executa se o arquivo for rodado diretamente.
if __name__ == "__main__":

    main()  # Chama a função principal