#JURIS-DATA-MINER
#Proibida a modificação ou uso comercial sem autorização expressa.
#Proibida reprodução, distribuição ou engenharia reversa sem autorização.
#Copyright © 2025 Lucas Rats. Todos os direitos reservados.

# Importa o módulo sys para manipulação do sistema (encerramento da aplicação, etc.)
import sys

# Importa QApplication do PyQt5 - a classe central que gerencia o aplicativo GUI
from PyQt5.QtWidgets import QApplication

# Importa nossa janela principal personalizada
from gui.main_window import MainWindow

# Define a função principal que será executada quando o script for chamado
def main():
    try:
        # Cria a instância QApplication, passando argumentos do sistema (sys.argv)
        app = QApplication(sys.argv)
        
        # Define o estilo visual para 'Fusion' - um estilo moderno que funciona em todas plataformas
        app.setStyle('Fusion')  

        # Cria uma instância da nossa janela personalizada (MainWindow)
        window = MainWindow()
        
        # Exibe a janela principal na tela
        window.show()
        
        # Inicia o loop de eventos da aplicação (app.exec_())
        # sys.exit() garante uma saída limpa quando a janela for fechada
        # Este comando bloqueia a execução até que a janela seja fechada
        sys.exit(app.exec_())
        
    except Exception as e:
        # Captura qualquer exceção não tratada durante a inicialização
        print(f"Erro ao iniciar a aplicação: {str(e)}")
        
        # Retorna código de erro 1 para o sistema operacional
        # Isso é útil se outro programa estiver chamando este script
        sys.exit(1)

# Verifica se este script está sendo executado diretamente
if __name__ == "__main__":
    # Chama nossa função principal
    main()

