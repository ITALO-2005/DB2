import persistent

class Autor(persistent.Persistent):
    def __init__(self, nome):
        self.nome = nome
        self.__livros = [] # Atributo para o relacionamento

    def adicionar_livro(self, livro):
        self.__livros.append(livro)
        self._p_changed = True

class Livro(persistent.Persistent):
    def __init__(self, titulo, ano):
        self.titulo = titulo
        self.ano = ano