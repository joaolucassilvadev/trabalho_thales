class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.componentes = []  # Lista para armazenar os componentes gramaticais

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
        """Inicia a análise sintática"""
        if self.S() and self.pos == len(self.tokens):
            print("✅ Frase aceita pela gramática!\n")
            print("📖 **Componentes Identificados:**")
            for palavra, tipo in self.componentes:
                print(f"🔹 {palavra}: {tipo}")
        else:
            print("❌ Erro sintático! A frase não segue a gramática.")

# Exemplo de uso
print("📚 Bem-vindo ao Analisador Sintático Automático!")
frase = input("✍️ Digite uma frase: ").lower().split()
analisador = AnalisadorSintatico(frase)
analisador.analisar()