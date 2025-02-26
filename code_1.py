# Importação das bibliotecas necessárias para a interface gráfica
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

class AnalisadorSintatico:
    """
    Classe responsável pela análise sintática da frase.
    Implementa uma gramática simples para análise de sentenças em português.
    """
    def __init__(self, tokens):
        # Inicializa o analisador com os tokens (palavras) da frase
        self.tokens = tokens  # Lista de palavras da frase
        self.pos = 0         # Posição atual na análise
        self.componentes = [] # Armazena os componentes gramaticais identificados

    def consumir(self, esperado, tipo):
        """Verifica se o próximo token é o esperado e avança, registrando o tipo gramatical."""
        if self.pos < len(self.tokens) and self.tokens[self.pos] == esperado:
            self.componentes.append((self.tokens[self.pos], tipo))
            self.pos += 1
            return True
        return False

    def SN(self):
        """Regra: SN → ART N | N"""
        if self.ART():
            if self.N():
                self.componentes.append(("SN", "Sujeito"))
                return True
        elif self.N():
            self.componentes.append(("SN", "Sujeito"))
            return True
        return False

    def VP(self):
        """Regra: VP → V SN | V"""
        if self.V():
            if self.SN():
                self.componentes.append(("VP", "Predicado"))
                return True
            self.componentes.append(("VP", "Predicado"))
            return True  # VP → V (sem SN)
        return False

    def S(self):
        """Regra: S → SN VP"""
        if self.SN():
            if self.VP():
                return True
        return False

    def ART(self):
        """Regra: ART → 'o' | 'a' | 'os' | 'as'"""
        return self.consumir("o", "Artigo") or self.consumir("a", "Artigo") or self.consumir("os", "Artigo") or self.consumir("as", "Artigo")

    def N(self):
        """Regra: N → QUALQUER_PALAVRA (assumimos que qualquer palavra pode ser um substantivo)"""
        if self.pos < len(self.tokens):
            self.componentes.append((self.tokens[self.pos], "Substantivo"))
            self.pos += 1
            return True
        return False

    def V(self):
        """Regra: V → QUALQUER_PALAVRA (assumimos que qualquer palavra pode ser um verbo)"""
        if self.pos < len(self.tokens):
            self.componentes.append((self.tokens[self.pos], "Verbo"))
            self.pos += 1
            return True
        return False

    def analisar(self):
        """Inicia a análise sintática e retorna o resultado formatado"""
        resultado = []
        if self.S() and self.pos == len(self.tokens):
            resultado.append("✅ Frase aceita pela gramática!\n")
            resultado.append("📖 **Componentes Identificados:**")
            for palavra, tipo in self.componentes:
                resultado.append(f"🔹 {palavra}: {tipo}")
        else:
            resultado.append("❌ Erro sintático! A frase não segue a gramática.")
        return "\n".join(resultado)

class AnalisadorInterface:
    """
    Classe responsável pela interface gráfica do analisador.
    Cria uma janela com campos para entrada de texto e exibição dos resultados.
    """
    def __init__(self):
        # Configuração da janela principal
        self.janela = tk.Tk()
        self.janela.title("Analisador Sintático Automático")
        self.janela.geometry("500x400")  # Define o tamanho inicial da janela
        
        # Configuração do estilo dos widgets
        style = ttk.Style()
        style.configure("TButton", padding=6)  # Estilo para botões
        style.configure("TLabel", padding=6)   # Estilo para labels
        
        # Criação do título da aplicação
        titulo = ttk.Label(self.janela, 
                          text="📚 Analisador Sintático Automático",
                          font=('Helvetica', 14, 'bold'))
        titulo.pack(pady=10)
        
        # Campo de instruções para o usuário
        instrucao = ttk.Label(self.janela, 
                             text="✍️ Digite uma frase para análise:")
        instrucao.pack()
        
        # Campo de entrada de texto
        self.entrada = ttk.Entry(self.janela, width=50)
        self.entrada.pack(pady=10)
        
        # Botão para iniciar a análise
        analisar_btn = ttk.Button(self.janela, 
                                 text="Analisar",
                                 command=self.realizar_analise)
        analisar_btn.pack(pady=5)
        
        # Área de texto rolável para exibir resultados
        self.resultado = scrolledtext.ScrolledText(self.janela, 
                                                 width=50, 
                                                 height=10,
                                                 wrap=tk.WORD)
        self.resultado.pack(pady=10, padx=10)
        
    def realizar_analise(self):
        """
        Método chamado quando o botão 'Analisar' é clicado.
        Obtém o texto da entrada, realiza a análise e exibe os resultados.
        """
        # Obter a frase da entrada e converter para minúsculas
        frase = self.entrada.get().lower().split()
        # Criar uma instância do analisador com a frase
        analisador = AnalisadorSintatico(frase)
        # Realizar a análise e obter o resultado
        resultado = analisador.analisar()
        
        # Limpar a área de resultado e inserir o novo resultado
        self.resultado.delete(1.0, tk.END)
        self.resultado.insert(tk.END, resultado)
    
    def iniciar(self):
        """Inicia o loop principal da interface gráfica"""
        self.janela.mainloop()

# Ponto de entrada do programa
if __name__ == "__main__":
    app = AnalisadorInterface()  # Cria uma instância da interface
    app.iniciar()               # Inicia a aplicação