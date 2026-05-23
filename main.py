import sqlite3


def criar_tabela():
    con = sqlite3.connect("finanças.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            valor REAL,
            tipo TEXT,
            data TEXT
        )
    """)
    con.commit()
    con.close()
    return None

def adicionar_transacao():
    descricao = input("Descrição: ")
    valor = float(input("Digite o valor: "))
    tipo = input("TIPO (receita/despesa): ")
    con = sqlite3.connect("finanças.db")
    cur = con.cursor()
    cur.execute("INSERT INTO transacoes (descricao, valor, tipo, data) VALUES (?, ?, ?, DATE('now'))", (descricao, valor, tipo))
    con.commit()
    con.close()
    print("Transação adicionada com sucesso")
    return None
    
def listar_transacoes():
    con = sqlite3.connect("finanças.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM transacoes")
    transacoes = cur.fetchall()
    con.close()
    if len(transacoes) == 0:
        print("nenhum registro encontrado.")
    else:
        for t in transacoes:
            print(f"id: {t[0]} | {t[1]} | R$ {t[2]:.2f} | {t[3]} | {t[4]}")
    return None

def calcular_saldo():
    con = sqlite3.connect("finanças.db")
    cur = con.cursor()
    cur.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'despesa'")
    despesas = cur.fetchone()[0]
    if despesas is None:
        despesa = 0 
    cur.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'receita'")
    receitas = cur.fetchone()[0]
    if receitas is None:
        receitas = 0
    saldo = receitas - despesas
    print(f"Receitas: R$ {receitas:.2f}") 
    print(f"Despesas : R$ {despesas :.2f}") 
    print(f"Saldo: R$ {saldo:.2f}") 
    con.close()

def deletar_transacao():
    listar_transacoes()
    id = int(input("Digite o ID da transação que deseja deletar: "))
    con = sqlite3.connect("finanças.db")
    cur = con.cursor()
    cur.execute("DELETE FROM transacoes WHERE id = ?", (id,))
    con.commit()
    con.close()
    print("Transação deletada com sucesso!")

def editar_transacao():
    listar_transacoes()
    id = int(input("Digite o ID da transação que deseja editar: "))
    descricao = input("Nova Descrição: ")
    valor = float(input("Novo valor: "))
    tipo = input("Novo tipo (receita/despesa): ")
    con = sqlite3.connect("finanças.db")
    cur = con.cursor()
    cur.execute("UPDATE transacoes SET descricao = ?, valor = ?, tipo = ? WHERE id = ?", (descricao, valor, tipo, id))
    con.commit()
    con.close()
    print("Transação editada com sucesso!")

def menu():
    criar_tabela()
    while True:
        print("\n=== GESTOR DE FINAÇAS ===")
        print("1 - Adicionar Transação")
        print("2 - Listar Transações")
        print("3 - Ver Saldo")
        print("4 - Deletar transação")
        print("5 - Editar transação")
        print("6 - sair")

        opcao = input("Escolha o que deseja fazer: ") 

        if opcao == "1":
            adicionar_transacao()
        elif opcao == "2":
            listar_transacoes()
        elif opcao == "3":
            calcular_saldo()
        elif opcao == "4":
            deletar_transacao()
        elif opcao == "5":
            editar_transacao()
        elif opcao =="6":
            print("Saindo... Obrigado por usar o sistema.")
            break
        else:
            print("Opção Inválida, Tente novamente.")
    
