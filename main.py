# JURIS-DATA-MINER
# Proibida a modificação ou uso comercial sem autorização expressa.
# Proibida reprodução, distribuição ou engenharia reversa sem autorização.
# Copyright © 2025 Lucas Rats. Todos os direitos reservados.

import sys
import logging
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from src.gui.main_window import MainWindow

def setup_logging():
    """Configura o sistema de logging para registrar erros e informações."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='juris_data_miner.log',
        filemode='a'
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    logging.getLogger().addHandler(console_handler)

def handle_exception(exc_type, exc_value, exc_traceback):
    """Captura exceções não tratadas e registra no log."""
    logging.error(
        "Exceção não tratada",
        exc_info=(exc_type, exc_value, exc_traceback)
    )
    QMessageBox.critical(
        None,
        "Erro Inesperado",
        f"Ocorreu um erro não tratado:\n\n{str(exc_value)}\n\nConsulte o arquivo de log para detalhes."
    )

def main():
    """Ponto de entrada principal da aplicação."""
    try:
        # Configura o logging
        setup_logging()
        
        # Configura handler para exceções não tratadas
        sys.excepthook = handle_exception
        
        # Cria a aplicação Qt
        app = QApplication(sys.argv)
        
        # Configurações globais da aplicação
        app.setStyle('Fusion')  # Estilo visual moderno
        app.setAttribute(Qt.AA_EnableHighDpiScaling)  # Suporte a High DPI
        app.setAttribute(Qt.AA_UseHighDpiPixmaps)  # Ícones em alta resolução
        
        # Cria e exibe a janela principal
        window = MainWindow()
        window.show()
        
        # Executa o loop principal
        return app.exec_()
        
    except Exception as e:
        logging.critical(f"Falha na inicialização: {str(e)}", exc_info=True)
        QMessageBox.critical(
            None,
            "Erro Fatal",
            f"Não foi possível iniciar a aplicação:\n\n{str(e)}\n\nVerifique o arquivo de log para detalhes."
        )
        return 1

if __name__ == "__main__":
    # Executa a aplicação e retorna o código de saída para o sistema
    sys.exit(main())