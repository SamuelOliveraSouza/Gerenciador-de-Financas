from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def conectar():
    con = sqlite3.connect("finanças.db")
    con.row_factory = sqlite3.Row
    return con

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/transacoes", methods=["GET"])

def listar():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM transacoes")
    dados = [dict(row) for row in cur.fetchall()]
    con.close()
    return jsonify(dados)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    dados = request.json
    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO transacoes (descricao, valor, tipo, data) VALUES (?, ?, ?, DATE('now'))", (dados["descricao"], dados["valor"], dados["tipo"]))
    con.commit()
    con.close()
    return jsonify({"mensagem": "transação adicionada"})

@app.route("/deletar/<int:id>", methods=["DELETE"])
def deletar(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM transacoes WHERE id = ?", (id,))
    con.commit()
    con.close()
    return jsonify({"mensagem": "Transaçaõ deleta com sucesso!"})

@app.route("/saldo", methods=["GET"])
def saldo():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT SUM(valor) as total FROM transacoes WHERE tipo =  'receita'")
    receitas = cur.fetchone()["total"] or 0
    cur.execute("SELECT SUM(valor) as total FROM transacoes WHERE tipo = 'despesa'")
    despesas = cur.fetchone()["total"] or 0
    con.close()
    return jsonify({"receitas": receitas, "despesas": despesas, "saldo": receitas - despesas})


@app.route("/editar/<int:id>", methods=["PUT"])
def editar(id):
    dados = request.json
    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE transacoes SET descricao = ?, valor = ?, tipo = ? WHERE id = ?", (dados["descricao"], dados["valor"], dados["tipo"], id ))
    con.commit()
    con.close()
    return jsonify({"mensagem": "Transação editada com sucesso"})


if __name__ == "__main__":
    from main import criar_tabela
    criar_tabela()
    app.run(debug=True)

