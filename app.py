from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import text
from sqlalchemy import create_engine
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://unbooklab_admin:senha@localhost:3306/Biblioteca'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chave'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_PASSWORD'] = 'password'

db = SQLAlchemy()

db.init_app(app)

engine = create_engine(
    'mysql://unbooklab_admin:senha@localhost:3306/Biblioteca'
)

#################################### HOME LOGIN #########################################################
'''
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/perform_login', methods=['POST'])
def perform_login():
    login = request.form.get('login')
    senha = request.form.get('senha')

    print("Login:", login) 
    print("Senha:", senha)
    user = db.session.execute(text("SELECT * FROM usuarios WHERE Login = :login AND SenhaCriptografada = :senha"), {'login': login, 'senha': senha}).fetchone()

    if user:
        return redirect(url_for('index'))

    else:
        return render_template('login.html', error="Login ou senha incorretos")

@app.route('/registrar')
def registrar():
    return render_template('registrar.html')

@app.route('/index')
def index():
    return render_template('index.html')
'''
######################################################################################################
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_livro', methods=['GET', 'POST'])
def add_livro():
    mensagem = None

    if request.method == 'POST':
        isbn = request.form['isbn']
        titulo = request.form['titulo']
        autor = request.form['autor']
        descricao = request.form['descricao']
        categoria = request.form['categoria']
        data_aquisicao = datetime.strptime(request.form['data_aquisicao'], '%Y-%m-%d').date()
        estado_conservacao = request.form['estado_conservacao']
        localizacao_fisica = request.form['localizacao_fisica']
        capa_livro_uri = request.form['capa_livro_uri']

        sql = text("""INSERT INTO livros (ISBN, Titulo, Autor, Descricao, Categoria, DataAquisicao, EstadoConservacao, LocalizacaoFisica, CapaLivroURI) 
                      VALUES (:isbn, :titulo, :autor, :descricao, :categoria, :data_aquisicao, :estado_conservacao, :localizacao_fisica, :capa_livro_uri)""")

        try:
            db.session.execute(sql, {
                'isbn': isbn,
                'titulo': titulo,
                'autor': autor,
                'descricao': descricao,
                'categoria': categoria,
                'data_aquisicao': data_aquisicao,
                'estado_conservacao': estado_conservacao,
                'localizacao_fisica': localizacao_fisica,
                'capa_livro_uri': capa_livro_uri
            })
            db.session.commit()
            mensagem = {'conteudo': 'Livro adicionado com sucesso!', 'classe': 'mensagem-sucesso'}
        except Exception as e:
            db.session.rollback()
            mensagem = {'conteudo': f'Erro ao adicionar o livro: {str(e)}', 'classe': 'mensagem-erro'}

    return render_template('cadastrar_livro.html', mensagem=mensagem)

@app.route('/update_livro', methods=['GET', 'POST'])
def update_livro():
    mensagem = None
    livro = None

    if request.method == 'POST':
        isbn_pesquisa = request.form.get('isbn_pesquisa')

        # Certifique-se de que ISBN não seja None antes de fazer a consulta
        if isbn_pesquisa is not None:
            livro = db.session.execute(text("SELECT * FROM livros WHERE ISBN = :isbn"), {'isbn': isbn_pesquisa}).fetchone()

        if livro:
            return redirect(url_for('update_livro_form', isbn=isbn_pesquisa))
        else:
            mensagem = {'conteudo': 'Livro não encontrado.',
                        'classe': 'mensagem-erro'}

    return render_template('update_livro_pesquisa.html', mensagem=mensagem)


@app.route('/update_livro/<isbn>', methods=['GET', 'POST'])
def update_livro_form(isbn):
    livro = db.session.execute(text("SELECT * FROM livros WHERE ISBN = :isbn"), {'isbn': isbn}).fetchone()
    mensagem = None

    if request.method == 'POST':
        if livro:
            data = request.form
            sql = text("""
                UPDATE livros
                SET Titulo = :titulo,
                    Autor = :autor,
                    Descricao = :descricao,
                    Categoria = :categoria,
                    DataAquisicao = :data_aquisicao,
                    EstadoConservacao = :estado_conservacao,
                    LocalizacaoFisica = :localizacao_fisica,
                    CapaLivroURI = :capa_livro_uri
                WHERE ISBN = :isbn
            """)

            try:
                db.session.execute(sql, {
                    'titulo': data.get('titulo', livro.Titulo),
                    'autor': data.get('autor', livro.Autor),
                    'descricao': data.get('descricao', livro.Descricao),
                    'categoria': data.get('categoria', livro.Categoria),
                    'data_aquisicao': datetime.strptime(data.get('data_aquisicao', str(livro.DataAquisicao)), '%Y-%m-%d').date(),
                    'estado_conservacao': data.get('estado_conservacao', livro.EstadoConservacao),
                    'localizacao_fisica': data.get('localizacao_fisica', livro.LocalizacaoFisica),
                    'capa_livro_uri': data.get('capa_livro_uri', livro.CapaLivroURI),
                    'isbn': isbn
                    })
                db.session.commit()
                mensagem = {'conteudo': 'Livro atualizado com sucesso!',
                            'classe': 'mensagem-sucesso'}
            except Exception as e:
                db.session.rollback()
                mensagem = {
                    'conteudo': f'Erro ao atualizar o livro: {str(e)}', 'classe': 'mensagem-erro'}
        else:
            mensagem = {
                'conteudo': 'Livro não encontrado para atualização.', 'classe': 'mensagem-erro'}

    return render_template('update_livro.html', livro=livro, mensagem=mensagem)


@app.route('/delete_livro', methods=['GET', 'POST'])
def delete_livro():
    mensagem = None
    livro = None

    if request.method == 'POST':
        isbn = request.form.get('isbn')
        livro = db.session.execute(text("SELECT * FROM livros WHERE ISBN = :isbn"), {'isbn': isbn}).fetchone()

        if livro:
            sql = text("DELETE FROM livros WHERE ISBN = :isbn")

            try:
                db.session.execute(sql, {'isbn': isbn})
                db.session.commit()
                mensagem = {'conteudo': 'Livro excluído com sucesso!',
                            'classe': 'mensagem-sucesso'}
            except Exception as e:
                db.session.rollback()
                mensagem = {
                    'conteudo': f'Erro ao excluir o livro: {str(e)}', 'classe': 'mensagem-erro'}
        else:
            mensagem = {
                'conteudo': 'Livro não encontrado para exclusão.', 'classe': 'mensagem-erro'}

    return render_template('delete_livro.html', livro=livro, mensagem=mensagem)


@app.route('/get_livro', methods=['GET', 'POST'])
def get_livro():
    if request.method == 'POST':
        isbn = request.form.get('isbn')

        if not isbn:
            return jsonify({'error': 'ISBN não fornecido'}), 400

        sql = text(
            """SELECT * FROM livros WHERE ISBN = :isbn"""
        )

        livro = db.session.execute(sql, {'isbn': isbn}).fetchone()

        if livro is None:
            return jsonify({'error': 'Livro não encontrado'}), 404

        livro_json = {
            'ISBN': livro.ISBN,
            'Titulo': livro.Titulo,
            'Autor': livro.Autor,
            'Descricao': livro.Descricao,
            'Categoria': livro.Categoria,
            'DataAquisicao': str(livro.DataAquisicao),
            'EstadoConservacao': livro.EstadoConservacao,
            'LocalizacaoFisica': livro.LocalizacaoFisica,
            'CapaLivroURI': livro.CapaLivroURI
        }

        return jsonify(livro_json)

    return render_template('get_livro.html')


@app.route('/get_livros')
def get_livros():
    sql = text(
        """SELECT ISBN, Titulo, Autor FROM livros"""
    )

    livros = db.session.execute(sql).fetchall()

    livros_json = [{'ISBN': livro.ISBN, 'Titulo': livro.Titulo,
                    'Autor': livro.Autor} for livro in livros]
    
    return jsonify(livros_json)


@app.route('/livros_crud')
def livros_crud():
    return render_template('livros_crud.html')

####### material didatico ########################################################################################################


@app.route('/add_material', methods=['GET', 'POST'])
def add_material():
    mensagem = None

    if request.method == 'POST':
        descricao = request.form['descricao']
        categoria = request.form['categoria']
        numero_serie = request.form['numero_serie']
        estado_conservacao = request.form['estado_conservacao']
        localizacao_fisica = request.form['localizacao_fisica']
        foto_material_uri = request.form['foto_material_uri']
 
        sql = text(
            """INSERT INTO materiaisdidaticos (Descricao, Categoria, NumeroSerie, EstadoConservacao, LocalizacaoFisica, FotoMaterialURI) 
            VALUES ('{descricao}', '{categoria}', '{numero_serie}', '{estado_conservacao}', '{localizacao_fisica}', '{foto_material_uri}');""".format(
                descricao=descricao, categoria=categoria, numero_serie=numero_serie,
                estado_conservacao=estado_conservacao, localizacao_fisica=localizacao_fisica, foto_material_uri=foto_material_uri))
        print(sql)

        try:
            db.session.execute(sql)
            db.session.commit()
            mensagem = {'conteudo': 'Material didático adicionado com sucesso!', 'classe': 'mensagem-sucesso'}
        except Exception as e:
            db.session.rollback()
            mensagem = {'conteudo': f'Erro ao adicionar o material didático: {str(e)}', 'classe': 'mensagem-erro'}

    return render_template('cadastrar_material.html', mensagem=mensagem)


@app.route('/update_material', methods=['GET', 'POST'])
def update_material():
    mensagem = None
    material = None

    if request.method == 'POST':
        id_pesquisa = request.form.get('id_pesquisa')
        # Certifique-se de que ID não seja None antes de fazer a consulta
        if id_pesquisa is not None:
            material = db.session.execute(text("SELECT * FROM materiaisdidaticos WHERE ID = :id"), {'id': id_pesquisa}).fetchone()

        if material:
            return redirect(url_for('update_material_form', id=id_pesquisa))
        else:
            mensagem = {'conteudo': 'Material didático não encontrado.', 'classe': 'mensagem-erro'}

    return render_template('update_material_pesquisa.html', mensagem=mensagem)

@app.route('/update_material/<id>', methods=['GET', 'POST'])
def update_material_form(id):
    material = db.session.execute(text("SELECT * FROM materiaisdidaticos WHERE ID = :id"), {'id': id}).fetchone()
    mensagem = None

    if request.method == 'POST':
        if material:
            data = request.form
            sql = text("""
                UPDATE materiaisdidaticos
                SET Descricao = :descricao,
                    Categoria = :categoria,
                    NumeroSerie = :numero_serie,
                    EstadoConservacao = :estado_conservacao,
                    LocalizacaoFisica = :localizacao_fisica,
                    FotoMaterialURI = :foto_material_uri
                WHERE ID = :id
            """)

            try:
                db.session.execute(sql, {
                    'descricao': data.get('descricao', material.Descricao),
                    'categoria': data.get('categoria', material.Categoria),
                    'numero_serie': data.get('numero_serie', material.NumeroSerie),
                    'estado_conservacao': data.get('estado_conservacao', material.EstadoConservacao),
                    'localizacao_fisica': data.get('localizacao_fisica', material.LocalizacaoFisica),
                    'foto_material_uri': data.get('foto_material_uri', material.FotoMaterialURI),
                    'id': id
                })
                db.session.commit()
                mensagem = {'conteudo': 'Material didático atualizado com sucesso!', 'classe': 'mensagem-sucesso'}
            except Exception as e:
                db.session.rollback()
                mensagem = {'conteudo': f'Erro ao atualizar o material didático: {str(e)}', 'classe': 'mensagem-erro'}
        else:
            mensagem = {'conteudo': 'Material didático não encontrado para atualização.', 'classe': 'mensagem-erro'}

    return render_template('update_material.html', material=material, mensagem=mensagem)



@app.route('/delete_material', methods=['GET', 'POST'])
def delete_material():
    mensagem = None
    material = None

    if request.method == 'POST':
        id = request.form.get('id')
        material = db.session.execute(text("SELECT * FROM materiaisdidaticos WHERE ID = :id"), {'id': id}).fetchone()

        if material:
            sql = text("DELETE FROM materiaisdidaticos WHERE ID = :id")

            try:
                db.session.execute(sql, {'id': id})
                db.session.commit()
                mensagem = {
                    'conteudo': 'Material didático excluído com sucesso!', 'classe': 'mensagem-sucesso'}
            except Exception as e:
                db.session.rollback()
                mensagem = {
                    'conteudo': f'Erro ao excluir o material didático: {str(e)}', 'classe': 'mensagem-erro'}
        else:
            mensagem = {
                'conteudo': 'Material didático não encontrado para exclusão.', 'classe': 'mensagem-erro'}

    return render_template('delete_material.html', material=material, mensagem=mensagem)


@app.route('/get_material', methods=['GET', 'POST'])
def get_material():
    if request.method == 'POST':
        id = request.form.get('id')

        if not id:
            return jsonify({'error': 'ID não fornecido'}), 400

        sql = text(
            """SELECT * FROM materiaisdidaticos WHERE ID = :id"""
        )

        material = db.session.execute(sql, {'id': id}).fetchone()

        if material is None:
            return jsonify({'error': 'Material didático não encontrado'}), 404

        material_json = {
            'ID': material.ID,
            'Descricao': material.Descricao,
            'Categoria': material.Categoria,
            'NumeroSerie': material.NumeroSerie,
            'EstadoConservacao': material.EstadoConservacao,
            'LocalizacaoFisica': material.LocalizacaoFisica,
            'FotoMaterialURI': material.FotoMaterialURI
        }

        return jsonify(material_json)

    return render_template('get_material.html')


@app.route('/get_materiais')
def get_materiais():
    sql = text(
        """SELECT ID, Descricao, Categoria FROM materiaisdidaticos"""
    )

    materiais = db.session.execute(sql).fetchall()

    materiais_json = [{'ID': material.ID, 'Descricao': material.Descricao,
                       'Categoria': material.Categoria} for material in materiais]
    return jsonify(materiais_json)

@app.route('/materiais_crud')
def materiais_crud():
    return render_template('material_crud.html')

# Usuarios ---------------------------------------------------


@app.route('/add_usuario', methods=['POST'])
def add_usuario():
    try:
        db.session.execute(text("""
            INSERT INTO usuarios (Nome, Sobrenome, Funcao, Login, SenhaCriptografada, FotoUsuarioURI)
            VALUES (:nome, :sobrenome, :funcao, :login, :senha, :foto)
        """), {
            'nome': 'name',
            'sobrenome': 'last name',
            'funcao': 'function',
            'login': 'login',
            'senha': 'password',
            'foto': 'photo'
        })
        db.session.commit()
        return 'Usuário adicionado com sucesso!'
    except Exception as e:
        db.session.rollback()
        return f'Erro ao adicionar usuário: {str(e)}'



@app.route('/update_usuario/<id>', methods=['PUT'])
def update_usuario(id):
    user_existente = db.session.execute(text("SELECT * FROM usuarios WHERE ID = :id"), {'id': id}).fetchone()

    if user_existente:
        data = request.json
        try:
            db.session.execute(text("""
                UPDATE usuarios
                SET Nome = :nome,
                    Sobrenome = :sobrenome,
                    Funcao = :funcao,
                    Login = :login,
                    SenhaCriptografada = :senha,
                    FotoUsuarioURI = :foto
                WHERE ID = :id
            """), {
                'nome': data.get('Nome', user_existente.Nome),
                'sobrenome': data.get('Sobrenome', user_existente.Sobrenome),
                'funcao': data.get('Funcao', user_existente.Funcao),
                'login': data.get('Login', user_existente.Login),
                'senha': data.get('SenhaCriptografada', user_existente.SenhaCriptografada),
                'foto': data.get('FotoUsuarioURI', user_existente.FotoUsuarioURI),
                'id': id
            })
            db.session.commit()
            return jsonify({'message': 'Usuário atualizado com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Usuário não encontrado'}), 404


@app.route('/delete_usuario/<id>', methods=['DELETE'])
def delete_usuario(id):
    user_existente = db.session.execute(text("SELECT * FROM usuarios WHERE ID = :id"), {'id': id}).fetchone()

    if user_existente:
        try:
            db.session.execute(text("DELETE FROM usuarios WHERE ID = :id"), {'id': id})
            db.session.commit()
            return jsonify({'message': 'Usuário excluído com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Usuário não encontrado'}), 404



@app.route('/get_usuario/<id>')
def get_usuario(id):
    user = db.session.execute(text("SELECT * FROM usuarios WHERE ID = :id"), {'id': id}).fetchone()

    if user:
        user_json = {
            'Nome': user.Nome,
            'Sobrenome': user.Sobrenome,
            'Funcao': user.Funcao,
            'Login': user.Login,
            'SenhaCriptografada': user.SenhaCriptografada,
            'FotoUsuarioURI': user.FotoUsuarioURI
        }
        return jsonify(user_json)
    else:
        return jsonify({'error': 'Usuário não encontrado'}), 404


# Emprestimos ---------------------------------------------


@app.route('/add_emprestimo', methods=['GET', 'POST'])
def add_emprestimo():
    mensagem = None
    if request.method == 'POST':
        user = request.form['user']
        livro = request.form['book']
        material = request.form['material']
        data_emp = request.form['data_emprestimo']
        data_dev = request.form['data_devolucao']
        status = request.form['status']
        sql = text(
            """INSERT INTO emprestimo (IDUsuario, IDLivro, IDMaterialDidatico, DataEmprestimo, DataDevolucaoPrevista, Status) 
            VALUES ({user}, {livro}, {material}, '{data_emp}', '{data_dev}', '{status}');""".format(
                user=user, livro=livro, material=material, data_emp=data_emp, data_dev=data_dev, status=status))
        print(sql)
        try:
            engine.execute(sql)
            mensagem = {'conteudo': 'Emprestimo adicionado com sucesso!',
                        'classe': 'mensagem-sucesso'}
        except Exception as e:
            db.session.rollback()
            mensagem = {
                'conteudo': f'Erro ao adicionar o livro: {str(e)}', 'classe': 'mensagem-erro'}

    return render_template('cadastrar_emprestimo.html', mensagem=mensagem)


@app.route('/update_emprestimo/<id>', methods=['PUT'])
def update_emprestimo(id):
    emprestimo = db.session.execute(text("SELECT * FROM emprestimos WHERE ID = :id"), {'id': id}).fetchone()
    if emprestimo is None:
        return jsonify({'error': 'Emprestimo não encontrado'}), 404

    data = request.json
    emprestimo.Login = data.get('DataEmprestimo', emprestimo.DataEmprestimo)
    emprestimo.DataDevolucaoPrevista = data.get(
        "2017-01-01", emprestimo.DataDevolucaoPrevista)
    emprestimo.Status = data.get('Status', emprestimo.Status)

    db.session.commit()
    return jsonify({'message': 'Emprestimo atualizado com sucesso'}), 200


@app.route('/delete_emprestimo/<id>', methods=['DELETE'])
def delete_emprestimo(id):
    emprestimo = db.session.execute(text("SELECT * FROM emprestimos WHERE ID = :id"), {'id': id}).fetchone()
    if emprestimo is None:
        return jsonify({'error': 'Emprestimo não encontrado'}), 404

    db.session.delete(emprestimo)
    db.session.commit()
    return jsonify({'message': 'Emprestimo excluído com sucesso'}), 200


@app.route('/get_emprestimo/<id>')
def get_emprestimo(id):
    emprestimo = db.session.execute(text("SELECT * FROM emprestimos WHERE ID = :id"), {'id': id}).fetchone()
    if emprestimo is None:
        return jsonify({'error': 'Material não encontrado'}), 404

    emprestimo_json = {
        'DataEmprestimo': emprestimo.DataEmprestimo,
        'DataDevolucaoPrevista': emprestimo.DataDevolucaoPrevista,
        'Status': emprestimo.Status,
    }

    return jsonify(emprestimo_json)


if __name__ == '__main__':
    app.run(debug=True)
