from flask import Flask, request, jsonify, render_template
from flask import session
from flask import redirect
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "eu_amo_loiras"

def conectar():
    con = sqlite3.connect("finanças.db")
    con.row_factory = sqlite3.Row
    return con

@app.route("/")
def index():
    if "usuario_id" not in session:
        return redirect("/login")
    else:
        return render_template("index.html")

@app.route("/transacoes", methods=["GET"])
def listar():
    usuario_id = session["usuario_id"]
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM transacoes WHERE usuario_id = ?", (usuario_id, ))
    dados = [dict(row) for row in cur.fetchall()]
    con.close()
    return jsonify(dados)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    if "usuario_id" not in session:
        return jsonify({"erro": "Faça login para continuar"}), 401
    usuario_id = session["usuario_id"]
    dados = request.json
    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO transacoes (descricao, valor, tipo, usuario_id, data) VALUES (?, ?, ?, ?, DATE('now'))", (dados["descricao"], dados["valor"], dados["tipo"], usuario_id))
    con.commit()
    con.close()
    return jsonify({"mensagem": "transação adicionada"})

@app.route("/deletar/<int:id>", methods=["DELETE"])
def deletar(id):
    if "usuario_id" not in session:
        return jsonify({"erro": "Faça login para continuar"}), 401
    usuario_id = session["usuario_id"]
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM transacoes WHERE id = ? AND usuario_id = ?", (id, usuario_id, ))
    con.commit()
    con.close()
    return jsonify({"mensagem": "Transaçaõ deleta com sucesso!"})

@app.route("/saldo", methods=["GET"])
def saldo():
    if "usuario_id" not in session:
        return jsonify({"erro": "Faça login para continuar"}), 401
    usuario_id = session["usuario_id"]
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT SUM(valor) as total FROM transacoes WHERE tipo =  'receita' AND usuario_id = ?", (usuario_id, ))
    receitas = cur.fetchone()["total"] or 0
    cur.execute("SELECT SUM(valor) as total FROM transacoes WHERE tipo = 'despesa' AND usuario_id = ?", (usuario_id, ))
    despesas = cur.fetchone()["total"] or 0
    con.close()
    return jsonify({"receitas": receitas, "despesas": despesas, "saldo": receitas - despesas})


@app.route("/editar/<int:id>", methods=["PUT"])
def editar(id):
    if "usuario_id" not in session:
        return jsonify({"erro": "Faça login para continuar"}), 401
    usuario_id = session["usuario_id"]
    dados = request.json
    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE transacoes SET descricao = ?, valor = ?, tipo = ? WHERE id = ? AND usuario_id = ?", (dados["descricao"], dados["valor"], dados["tipo"], id, usuario_id ))
    con.commit()
    con.close()
    return jsonify({"mensagem": "Transação editada com sucesso"})

@app.route("/logout")
def logout():
    session.clear()
    return jsonify({"mensagem": "Logout feito com sucesso!"})

@app.route("/login", methods=["GET", "POST"])
def html_login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        dados = request.json
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = ?", (dados["email"],))
        usuarios = cur.fetchone()
        if usuarios is None:
            return jsonify({"ERRO": "Email não encontrado"})
        if not check_password_hash(usuarios["senha"], dados["senha"]):
            return jsonify({"ERRO": "Senha Incorreta!"})
        con.close()
        session["usuario_id"] = usuarios["id"]
        session["usuario_nome"] = usuarios["nome"]
        return jsonify({"mensagem": "Login efetuado com sucesso!"})

@app.route("/cadastro", methods=["GET", "POST"])
def html_cadastrar():
    if request.method == "GET":
        return render_template("cadastro.html")
    else:
        dados = request.json
        con = conectar()
        cur = con.cursor()
        senha_criptografada = generate_password_hash(dados["senha"])
        cur.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (dados["nome"], dados["email"], senha_criptografada))
        con.commit()
        con.close()
        return jsonify({"mensagem": "Cadastro feito com sucesso!"})

if __name__ == "__main__":
    from main import criar_tabela, criar_tabela_usuarios
    criar_tabela()
    criar_tabela_usuarios()
    app.run(debug=True)

