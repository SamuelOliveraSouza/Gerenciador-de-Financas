import tkinter as tk 
from tkinter import ttk, messagebox
from main import adicionar_transacao, listar_transacoes, calcular_saldo, deletar_transacao, editar_transacao, criar_tabela

criar_tabela()

janela = tk.Tk()
janela.title("Gestor de Finanças")
janela.geometry("700x500")

tabela = ttk.Treeview(janela, columns=("ID", "Descrição", "Valor", "Tipo", "Data"), show="headings")
tabela.heading("ID", text="ID")
tabela.heading("Descrição", text="Descrição")
tabela.heading("Valor", text="Valor")
tabela.heading("Tipo", text="Tipo")
tabela.heading("Data", text="Data")

tabela.column("ID", width=30)
tabela.column("Descrição", width=200)
tabela.column("Valor", width=100)
tabela.column("Tipo", width=100)
tabela.column("Data", width=100)

tabela.pack(pady=10)

def carregar_dados():
    for linha in tabela.get_children():
        tabela.delete(linha)
    import sqlite3
    con = sqlite3.connect("finanças.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM transacoes")
    for row in cur.fetchall():
        tabela.insert("", "end", values=row)
    con.close()

frame = tk.Frame(janela)
frame.pack(pady=10)

tk.Label(frame, text="Descrição:").grid(row=0, column=0, padx=5)
entrada_descricao = tk.Entry(frame, width=20)
entrada_descricao.grid(row=0, column=1, padx=5)

tk.Label(frame, text="Valor: ").grid(row=0, column=2, padx=5)
entrada_valor = tk.Entry(frame, width=10)
entrada_valor.grid(row=0, column=3, padx=5)

tk.Label(frame, text="Tipo: ").grid(row=0, column=4, padx=5)
entrada_tipo = tk.Entry(frame, width=10)
entrada_tipo.grid(row=0, column=5, padx=5)


def adicionar():
    descricao = entrada_descricao.get()
    valor = entrada_valor.get()
    tipo = entrada_tipo.get()

    if descricao == "" or valor == "" or tipo == "":
        messagebox.showwarning("atenção", "Preencha todos os campos!")
        return
    
    import sqlite3
    con = sqlite3.connect("finanças.db")
    cur = con.cursor()
    cur.execute("INSERT INTO transacoes (descricao, valor, tipo, data) VALUES (?,?,?, DATE('now'))", (descricao, float(valor), tipo))
    con.commit()
    con.close()

    entrada_descricao.delete(0, tk.END)
    entrada_valor.delete(0, tk.END)
    entrada_tipo.delete(0, tk.END)

    carregar_dados()
    messagebox.showinfo("Sucesso", "Transação adicionada!")

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=5)

tk.Button(frame_botoes, text="Adicionar", command=adicionar).grid(row=0, column=0, padx=5)
tk.Button(frame_botoes, text="Atualizar lista", command=carregar_dados).grid(row=0, column=1, padx=5)

def deletar():
    selecionado = tabela.focus()
    if selecionado == "":
        messagebox.showwarning("Atenção", "Selecione uma transaçaõ na tabela!")
        return
    
    valores = tabela.item(selecionado, "values")
    id = valores[0]

    confirmacao = messagebox.askyesno("Confirmar", f"Deseja deletar a transação '{valores[1]}'")
    if confirmacao:
        import sqlite3
        con = sqlite3.connect("finanças.db")
        cur = con.cursor()
        cur.execute("DELETE FROM transacoes WHERE id = ?", (id,) )
        con.commit()
        con.close()
        carregar_dados()
        messagebox.showinfo("Sucesso", "Transação Deletada!")

def ver_saldo():
    import sqlite3
    con = sqlite3.connect("finanças.db")
    cur = con.cursor()
    cur.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'receita'")
    receitas = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(valor) FROM transacoes WHERE  tipo = 'despesa'")
    despesas = cur.fetchone()[0] or 0

    con.close()
    saldo = receitas - despesas
    messagebox.showinfo("saldo", f"Receitas: r$ {receitas:.2f}\nDespesas: R$ {despesas:.2f}\nSaldo: R$ {saldo:.2f}")

tk.Button(frame_botoes, text="Deletar Selecionado", command=deletar).grid(row=0, column=2, padx=5)
tk.Button(frame_botoes, text="ver saldo", command=ver_saldo).grid(row=0, column=3, padx=5)



carregar_dados()
janela.mainloop()