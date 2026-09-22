# =========================================================
# APP.PY
# CORINTHIANS ARCHIVE STUDIES
# =========================================================

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for
)

from functools import wraps
from dotenv import load_dotenv

import psycopg2
import unicodedata
import hmac
import os
import re


# =========================================================
# VARIÁVEIS DE AMBIENTE
# =========================================================

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


if not SECRET_KEY:
    raise RuntimeError(
        'SECRET_KEY não foi configurada no arquivo .env'
    )


if not ADMIN_PASSWORD:
    raise RuntimeError(
        'ADMIN_PASSWORD não foi configurada no arquivo .env'
    )


# =========================================================
# CRIAÇÃO DO APP
# =========================================================

app = Flask(__name__)

app.secret_key = SECRET_KEY

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)


# =========================================================
# CONEXÃO COM O BANCO
# =========================================================

def conectar_banco():

    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode='require'
    )


# =========================================================
# AUTENTICAÇÃO ADMINISTRATIVA
# =========================================================

def admin_required(funcao):

    @wraps(funcao)
    def wrapper(*args, **kwargs):

        if not session.get('admin_authenticated'):

            return redirect(
                url_for('login')
            )

        return funcao(
            *args,
            **kwargs
        )

    return wrapper


# =========================================================
# ORDEM CURATORIAL DAS FAMÍLIAS
# =========================================================

ORDEM_FAMILIAS = [
    'PAVILHÃO',
    'YOKOHAMA',
    'DEMOCRACIA',
    '1910',
    'SCCP STUDIES'
]


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def extrair_familia(colecao):

    if not colecao:
        return 'SEM COLEÇÃO'

    return colecao.split('/')[0].strip().upper()


def gerar_slug(texto):

    texto = unicodedata.normalize(
        'NFKD',
        texto
    )

    texto = texto.encode(
        'ascii',
        'ignore'
    ).decode('ascii')

    texto = texto.lower()

    texto = re.sub(
        r'[^a-z0-9]+',
        '-',
        texto
    )

    return texto.strip('-')


def organizar_familias(produtos):

    familias = {}

    for produto in produtos:

        colecao = produto[4] or 'SEM COLEÇÃO'

        nome_familia = extrair_familia(
            colecao
        )

        if nome_familia not in familias:

            familias[nome_familia] = {
                'nome': nome_familia,
                'colecao': colecao,
                'slug': gerar_slug(nome_familia),
                'produtos': []
            }

        familias[nome_familia]['produtos'].append(
            produto
        )

    # -----------------------------------------------------
    # ORDENA AS PEÇAS DENTRO DE CADA FAMÍLIA
    # -----------------------------------------------------

    for familia in familias.values():

        familia['produtos'].sort(
            key=lambda produto: produto[0]
        )

    # -----------------------------------------------------
    # ORDEM CURATORIAL DAS FAMÍLIAS
    # -----------------------------------------------------

    def ordem(familia):

        nome = familia['nome']

        if nome in ORDEM_FAMILIAS:

            return (
                ORDEM_FAMILIAS.index(nome),
                nome
            )

        return (
            len(ORDEM_FAMILIAS),
            nome
        )

    return sorted(
        familias.values(),
        key=ordem
    )


# =========================================================
# HOME / ARCHIVE INDEX
# =========================================================

@app.route('/')
def home():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT *
        FROM produtos
        ORDER BY id ASC
        """
    )

    produtos = cursor.fetchall()

    cursor.close()
    conexao.close()

    familias = organizar_familias(
        produtos
    )

    return render_template(
        'index.html',
        produtos=produtos,
        familias=familias
    )


# =========================================================
# PÁGINA INDIVIDUAL DA PEÇA
# =========================================================

@app.route('/produto/<int:id>')
def produto(id):

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT *
        FROM produtos
        WHERE id = %s
        """,
        (id,)
    )

    produto = cursor.fetchone()

    cursor.close()
    conexao.close()

    if produto is None:
        return redirect('/')

    return render_template(
        'produto.html',
        produto=produto
    )


# =========================================================
# LOGIN ADMINISTRATIVO
# =========================================================

@app.route(
    '/login',
    methods=['GET', 'POST']
)
def login():

    if session.get('admin_authenticated'):

        return redirect(
            url_for('admin')
        )

    erro = None

    if request.method == 'POST':

        senha = request.form.get(
            'senha',
            ''
        )

        senha_correta = hmac.compare_digest(
            senha.encode('utf-8'),
            ADMIN_PASSWORD.encode('utf-8')
        )

        if senha_correta:

            session.clear()

            session['admin_authenticated'] = True

            return redirect(
                url_for('admin')
            )

        erro = 'ACCESS DENIED / INVALID CREDENTIAL'

    return render_template(
        'login.html',
        erro=erro
    )


# =========================================================
# LOGOUT ADMINISTRATIVO
# =========================================================

@app.route('/logout')
def logout():

    session.clear()

    return redirect(
        url_for('login')
    )


# =========================================================
# ADMIN
# =========================================================

@app.route('/admin')
@admin_required
def admin():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT *
        FROM produtos
        ORDER BY id ASC
        """
    )

    produtos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        'admin.html',
        produtos=produtos
    )


# =========================================================
# CADASTRAR PEÇA
# =========================================================

@app.route(
    '/cadastrar',
    methods=['POST']
)
@admin_required
def cadastrar():

    nome = request.form['nome']
    preco = request.form['preco']
    descricao = request.form['descricao']

    colecao = request.form.get(
        'colecao',
        ''
    )

    temporada = request.form.get(
        'temporada',
        ''
    )

    categoria = request.form.get(
        'categoria',
        ''
    )

    tags = request.form.get(
        'tags',
        ''
    )

    imagem = request.form.get(
        'imagem',
        ''
    )

    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO produtos (
            nome,
            preco,
            descricao,
            colecao,
            temporada,
            categoria,
            tags,
            imagem
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """

    valores = (
        nome,
        preco,
        descricao,
        colecao,
        temporada,
        categoria,
        tags,
        imagem
    )

    cursor.execute(
        sql,
        valores
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect(
        url_for('admin')
    )


# =========================================================
# EDITAR PEÇA
# =========================================================

@app.route(
    '/editar/<int:id>',
    methods=['GET', 'POST']
)
@admin_required
def editar(id):

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # =====================================================
    # POST
    # =====================================================

    if request.method == 'POST':

        nome = request.form['nome']
        preco = request.form['preco']
        descricao = request.form['descricao']

        colecao = request.form.get(
            'colecao',
            ''
        )

        temporada = request.form.get(
            'temporada',
            ''
        )

        categoria = request.form.get(
            'categoria',
            ''
        )

        tags = request.form.get(
            'tags',
            ''
        )

        imagem = request.form.get(
            'imagem',
            ''
        )

        sql = """
            UPDATE produtos
            SET
                nome = %s,
                preco = %s,
                descricao = %s,
                colecao = %s,
                temporada = %s,
                categoria = %s,
                tags = %s,
                imagem = %s
            WHERE id = %s
        """

        valores = (
            nome,
            preco,
            descricao,
            colecao,
            temporada,
            categoria,
            tags,
            imagem,
            id
        )

        cursor.execute(
            sql,
            valores
        )

        conexao.commit()

        cursor.close()
        conexao.close()

        return redirect(
            url_for('admin')
        )

    # =====================================================
    # GET
    # =====================================================

    cursor.execute(
        """
        SELECT *
        FROM produtos
        WHERE id = %s
        """,
        (id,)
    )

    produto = cursor.fetchone()

    cursor.close()
    conexao.close()

    if produto is None:

        return redirect(
            url_for('admin')
        )

    return render_template(
        'editar.html',
        produto=produto
    )


# =========================================================
# DELETAR PEÇA
# =========================================================

@app.route(
    '/deletar/<int:id>',
    methods=['POST']
)
@admin_required
def deletar(id):

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        DELETE FROM produtos
        WHERE id = %s
        """,
        (id,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect(
        url_for('admin')
    )


# =========================================================
# EXECUTA SERVIDOR
# =========================================================

if __name__ == '__main__':

    app.run(
        debug=True
    )