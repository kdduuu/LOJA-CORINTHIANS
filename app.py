# =========================================================
# APP.PY
# =========================================================

# Importações Flask
from flask import Flask, render_template, request, redirect

# Importação MySQL
import mysql.connector


# =========================================================
# CRIAÇÃO APP
# =========================================================

app = Flask(__name__)


# =========================================================
# HOME
# =========================================================

@app.route('/')
def home():

    # =============================================
    # CONEXÃO MYSQL
    # =============================================

    conexao = mysql.connector.connect(

        host='localhost',

        user='root',

        password='',

        database='loja_corinthians'
    )

    # Cursor executa SQL
    cursor = conexao.cursor()

    # Busca produtos
    cursor.execute("SELECT * FROM produtos")

    # Pega todos resultados
    produtos = cursor.fetchall()

    # Fecha conexão
    cursor.close()

    conexao.close()

    # Renderiza HTML
    return render_template(

        'index.html',

        produtos=produtos
    )


# =========================================================
# CADASTRAR PRODUTO
# =========================================================

@app.route('/cadastrar', methods=['POST'])

def cadastrar():

    # Dados formulário
    nome = request.form['nome']

    preco = request.form['preco']

    descricao = request.form['descricao']

    # =============================================
    # CONEXÃO MYSQL
    # =============================================

    conexao = mysql.connector.connect(

        host='localhost',

        user='root',

        password='',

        database='loja_corinthians'
    )

    cursor = conexao.cursor()

    # SQL INSERT
    sql = """

    INSERT INTO produtos (nome, preco, descricao)

    VALUES (%s, %s, %s)

    """

    # Executa SQL
    cursor.execute(

        sql,

        (nome, preco, descricao)
    )

    # Salva no banco
    conexao.commit()

    # Fecha conexão
    cursor.close()

    conexao.close()

    # Volta para home
    return redirect('/')


# =========================================================
# DELETAR PRODUTO
# =========================================================

@app.route('/deletar/<int:id>')

def deletar(id):

    # =============================================
    # CONEXÃO MYSQL
    # =============================================

    conexao = mysql.connector.connect(

        host='localhost',

        user='root',

        password='',

        database='loja_corinthians'
    )

    cursor = conexao.cursor()

    # SQL DELETE
    sql = "DELETE FROM produtos WHERE id = %s"

    # Executa SQL
    cursor.execute(sql, (id,))

    # Salva alteração
    conexao.commit()

    # Fecha conexão
    cursor.close()

    conexao.close()

    # Redireciona
    return redirect('/')


# =========================================================
# EDITAR PRODUTO
# =========================================================

@app.route('/editar/<int:id>', methods=['GET', 'POST'])

def editar(id):

    # =============================================
    # CONEXÃO MYSQL
    # =============================================

    conexao = mysql.connector.connect(

        host='localhost',

        user='root',

        password='',

        database='loja_corinthians'
    )

    cursor = conexao.cursor()

    # =====================================================
    # POST
    # =====================================================

    if request.method == 'POST':

        # Dados formulário
        nome = request.form['nome']

        preco = request.form['preco']

        descricao = request.form['descricao']

        # SQL UPDATE
        sql = """

        UPDATE produtos

        SET nome = %s,
            preco = %s,
            descricao = %s

        WHERE id = %s

        """

        # Executa SQL
        cursor.execute(

            sql,

            (nome, preco, descricao, id)
        )

        # Salva alterações
        conexao.commit()

        # Fecha conexão
        cursor.close()

        conexao.close()

        # Redireciona
        return redirect('/')


    # =====================================================
    # GET
    # =====================================================

    sql = "SELECT * FROM produtos WHERE id = %s"

    cursor.execute(sql, (id,))

    produto = cursor.fetchone()

    cursor.close()

    conexao.close()

    return render_template(

        'editar.html',

        produto=produto
    )


# =========================================================
# EXECUTA SERVIDOR
# =========================================================

if __name__ == '__main__':

    app.run(debug=True)