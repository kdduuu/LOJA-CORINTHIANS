# CORINTHIANS ARCHIVE STUDIES V2

Aplicação web desenvolvida com Flask para funcionar como um catálogo digital conceitual inspirado em archive fashion.

O projeto apresenta peças organizadas em famílias e coleções, páginas individuais para cada objeto do arquivo e uma área administrativa protegida para gerenciamento do catálogo.

> Projeto independente e não oficial.

---

## Live

Acesse o projeto online:

https://corinthians-archive-studies-v2.onrender.com

> O projeto utiliza o plano gratuito do Render. Caso esteja inativo há algum tempo, o primeiro acesso pode levar alguns segundos para carregar.

---

## Sobre o projeto

O CORINTHIANS ARCHIVE STUDIES V2 surgiu como uma evolução de uma aplicação simples de gerenciamento de produtos.

A proposta atual deixou de ser apenas uma loja e passou a funcionar como um arquivo digital experimental, combinando desenvolvimento web, organização de dados e uma direção visual inspirada em archive fashion e estética editorial.

As peças cadastradas são apresentadas como objetos de arquivo e organizadas em diferentes famílias e estudos.

---

## Funcionalidades

- Catálogo público de peças
- Organização por famílias e coleções
- Página individual para cada peça
- Exibição de informações como nome, preço, descrição, coleção, temporada, categoria, tags e imagem
- Área administrativa protegida por login
- Cadastro de novas peças
- Edição de peças existentes
- Exclusão de peças
- CRUD completo
- Interface responsiva
- Player de áudio integrado à experiência visual

---

## Tecnologias utilizadas

- Python
- Flask
- PostgreSQL
- Supabase
- Psycopg2
- HTML5
- CSS3
- JavaScript
- Jinja2
- Gunicorn
- Render
- Git
- GitHub

---

## Arquitetura

A aplicação segue uma arquitetura web cliente-servidor.

```text
Usuário
   ↓
Navegador
   ↓
Render
   ↓
Flask + Gunicorn
   ↓
Supabase
   ↓
PostgreSQL
```

O Flask é responsável pelas rotas, regras da aplicação, autenticação administrativa e comunicação com o banco de dados.

O PostgreSQL hospedado no Supabase armazena as informações das peças.

O Render executa a aplicação Flask e disponibiliza o sistema publicamente na internet.

---

## Banco de dados

A tabela principal do projeto é `produtos`.

Estrutura atual:

```text
id
nome
preco
descricao
colecao
temporada
categoria
tags
imagem
```

O campo `id` é gerado automaticamente pelo PostgreSQL e utilizado nas rotas individuais das peças.

---

## Área administrativa

O projeto possui uma área administrativa acessível através de autenticação.

Após o login, é possível:

- visualizar os objetos cadastrados;
- cadastrar novas peças;
- editar registros existentes;
- excluir registros.

As rotas administrativas são protegidas para impedir acesso direto sem autenticação.

As credenciais e informações sensíveis não são armazenadas diretamente no código. Elas são carregadas através de variáveis de ambiente.

---

## Organização do catálogo

As peças são agrupadas automaticamente em famílias a partir do campo `colecao`.

Exemplo:

```text
PAVILHÃO / SÃO PAULO
↓
família: PAVILHÃO
```

Entre as famílias atuais estão:

- PAVILHÃO
- YOKOHAMA
- DEMOCRACIA
- 1910
- SCCP STUDIES

A aplicação também utiliza uma ordem curatorial definida no backend para controlar como essas famílias aparecem no catálogo.

---

## Estrutura do projeto

```text
LOJA-CORINTHIANS/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── templates/
│   ├── index.html
│   ├── produto.html
│   ├── login.html
│   ├── admin.html
│   └── editar.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    ├── images/
    │
    └── audio/
```

O arquivo `.env` não é enviado ao GitHub e armazena informações sensíveis como credenciais administrativas e conexão com o banco.

---

## Fluxo do sistema

O fluxo principal da aplicação funciona da seguinte forma:

```text
Home
↓
Famílias / Coleções
↓
Peça individual
```

A área administrativa funciona assim:

```text
/login
↓
/admin
↓
Cadastrar / Editar / Excluir
↓
PostgreSQL
↓
Catálogo atualizado
```

---

## Flask e Jinja

O Flask funciona como o núcleo da aplicação.

Ele recebe as requisições do navegador, identifica a rota correspondente, executa a lógica necessária e consulta o banco de dados quando necessário.

Depois disso, os dados são enviados para os templates HTML através do Jinja.

Exemplo:

```python
return render_template(
    'index.html',
    produtos=produtos,
    familias=familias
)
```

Nesse caso, `produtos` e `familias` ficam disponíveis dentro do template `index.html`.

---

## CRUD

O projeto possui CRUD completo.

```text
CREATE
→ cadastrar uma nova peça

READ
→ visualizar o catálogo e páginas individuais

UPDATE
→ editar uma peça existente

DELETE
→ excluir uma peça
```

As operações são realizadas pelo Flask diretamente no PostgreSQL.

---

## Famílias e coleções

A função `extrair_familia()` identifica a família principal de uma coleção.

Exemplo:

```text
PAVILHÃO / STUDY 01
```

é interpretado como:

```text
PAVILHÃO
```

A função `organizar_familias()` agrupa os produtos e organiza a exibição de acordo com uma ordem curatorial definida no backend.

---

## Slugs

A função `gerar_slug()` transforma textos em identificadores simplificados.

Exemplo:

```text
SCCP STUDIES
```

vira:

```text
sccp-studies
```

A função remove acentos, transforma o texto em letras minúsculas e substitui caracteres inadequados por hífens.

---

## Autenticação

O sistema possui uma área administrativa protegida por autenticação.

Depois que a senha correta é informada, o Flask cria uma sessão:

```python
session['admin_authenticated'] = True
```

As rotas administrativas utilizam o decorator:

```python
@admin_required
```

Entre as rotas protegidas estão:

```text
/admin
/cadastrar
/editar/<id>
/deletar/<id>
```

---

## Variáveis de ambiente

Informações sensíveis não ficam diretamente no código.

Durante o desenvolvimento local, são armazenadas no arquivo `.env`.

Entre elas:

```env
SECRET_KEY=
ADMIN_PASSWORD=

DB_HOST=
DB_PORT=5432
DB_NAME=postgres
DB_USER=
DB_PASSWORD=
```

O arquivo `.env` está incluído no `.gitignore` e não é enviado ao GitHub.

No Render, essas mesmas informações são configuradas através das Environment Variables.

---

## Execução local

Para executar o projeto localmente, é necessário possuir Python instalado.

Crie um ambiente virtual:

```bash
python -m venv venv
```

No Windows, ative com:

```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure o arquivo `.env` com as variáveis necessárias.

Depois execute:

```bash
python app.py
```

A aplicação ficará disponível localmente em:

```text
http://127.0.0.1:5000
```

---

## Deploy

A versão online utiliza:

- Render para hospedagem da aplicação Flask
- Gunicorn como servidor de produção
- Supabase para hospedagem do PostgreSQL

O comando utilizado pelo Render para iniciar a aplicação é:

```bash
gunicorn app:app
```

Isso significa que o Gunicorn acessa o arquivo `app.py` e executa o objeto Flask chamado `app`.

---

## Segurança

O projeto utiliza algumas práticas básicas de segurança:

- senhas e credenciais armazenadas em variáveis de ambiente;
- `.env` ignorado pelo Git;
- autenticação administrativa baseada em sessão;
- rotas administrativas protegidas;
- conexão com PostgreSQL utilizando SSL;
- credenciais do banco fora do código-fonte.

---

## Sistema interativo, adaptável e distribuído

Atualmente, o CORINTHIANS ARCHIVE STUDIES V2 pode ser classificado principalmente como um sistema interativo.

O usuário interage diretamente com a aplicação ao navegar pelo catálogo, abrir peças e utilizar diferentes elementos da interface.

O sistema também possui características distribuídas, já que diferentes partes da aplicação funcionam em ambientes separados e se comunicam através da rede.

```text
Navegador
↓
Render
↓
Flask
↓
Supabase
↓
PostgreSQL
```

Uma das próximas etapas previstas para o projeto é a implementação de Machine Learning.

Com isso, o sistema também deverá incorporar características adaptáveis, utilizando dados e padrões de interação para adaptar ou personalizar parte da experiência do usuário.

---

## Machine Learning

Uma das próximas etapas previstas para o projeto é a implementação de Machine Learning.

A intenção é utilizar o projeto para estudar análise de dados, identificação de padrões e adaptação da experiência do usuário.

Essa funcionalidade ainda está em desenvolvimento e não faz parte da versão atual publicada.

---

## Objetivo

O projeto funciona como ambiente de estudo e aplicação prática de conceitos de desenvolvimento web.

Durante o desenvolvimento foram aplicados conceitos como:

- Python
- Flask
- rotas HTTP
- arquitetura cliente-servidor
- sistemas interativos
- sistemas distribuídos
- templates Jinja2
- CRUD
- PostgreSQL
- banco de dados em nuvem
- autenticação e sessões
- variáveis de ambiente
- responsividade
- HTML
- CSS
- JavaScript
- deploy de aplicações web
- versionamento com Git
- GitHub
- Render
- Supabase

O projeto também será utilizado futuramente para estudo e implementação de Machine Learning.

---

## Status do projeto

Atualmente estão concluídos:

- catálogo público;
- organização por famílias e coleções;
- página individual das peças;
- autenticação administrativa;
- CRUD completo;
- PostgreSQL em nuvem;
- migração do antigo MySQL para PostgreSQL;
- hospedagem no Render;
- integração entre Flask, Render e Supabase;
- site público funcional.

Próximas etapas:

- implementação de Machine Learning;
- evolução da experiência adaptável;
- refinamentos visuais;
- evolução das funcionalidades do catálogo.

---

## Autor

Desenvolvido por **Kadu Almeida**.