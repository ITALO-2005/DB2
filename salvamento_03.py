import ZODB, ZODB.FileStorage
import transaction
# Supondo que as classes Autor e Livro estão em um arquivo 'model.py'
from model import Autor, Livro

# --- 1. Conexão com o Banco de Dados ---
storage = ZODB.FileStorage.FileStorage('meu_banco.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

# --- 2. Preparação da Estrutura na Raiz ---
# Garante que a chave 'autores' exista como uma lista
if 'autores' not in root:
    root['autores'] = []

print(f"Autores existentes antes da transação: {len(root['autores'])}")

# --- 3. Criação das Instâncias dos Objetos ---
# Autor 1 e seus livros
autor_asimov = Autor("Isaac Asimov2")
livro_fundacao = Livro("Fundação2", 1951)
livro_robo = Livro("Eu, Robô2", 1950)

# Autor 2 e seu livro
autor_pkd = Autor("Philip K. Dick2")
livro_androides = Livro("Androides Sonham com Ovelhas Elétricas?2", 1968)

# --- 4. Estabelecimento dos Relacionamentos ---
# Adicionamos os objetos Livro à lista de livros de cada Autor
autor_asimov.adicionar_livro(livro_fundacao)
autor_asimov.adicionar_livro(livro_robo)

autor_pkd.adicionar_livro(livro_androides)

# --- 5. Adição dos Objetos Principais à Raiz ---
# Note que só precisamos adicionar os autores.
# Os livros serão salvos automaticamente por estarem referenciados pelos autores!
root['autores'].append(autor_asimov)
root['autores'].append(autor_pkd)
print("Novos autores e livros preparados para o commit.")

# --- 6. Commit Atômico da Transação ---
# Salva TUDO (os 2 autores e os 3 livros) de uma vez.
# Se ocorrer um erro aqui, NADA é salvo.
try:
    transaction.commit()
    print("Sucesso! Transação confirmada.")
    print(f"Autores existentes após a transação: {len(root['autores'])}")
except Exception as e:
    transaction.abort()
    print(f"Erro! A transação foi cancelada: {e}")

# --- 7. Fechamento da Conexão ---
finally:
    connection.close()
    db.close()