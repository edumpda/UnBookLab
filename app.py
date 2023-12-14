from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import text
from sqlalchemy import create_engine
import emprestimo_module
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:#teste123321@localhost:3306/Biblioteca'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chave'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_PASSWORD'] = 'password'

db = SQLAlchemy()

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user_data = db.session.execute(text(
        "SELECT * FROM Usuarios WHERE ID = :user_id"), {'user_id': user_id}).fetchone()
    if user_data:
        return User(
            user_id=user_data.ID,
            login=user_data.Login,
            sobrenome=user_data.Sobrenome,
            funcao=user_data.Funcao,
            foto_usuario_uri=user_data.FotoUsuarioURI
        )
    return None


class User(UserMixin):
    def __init__(self, user_id, login=None, sobrenome=None, funcao=None, foto_usuario_uri=None):
        self.id = user_id
        self.login = login
        self.sobrenome = sobrenome
        self.funcao = funcao
        self.foto_usuario_uri = foto_usuario_uri

    @staticmethod
    def get(user_id):
        user_data = db.session.execute(text(
            "SELECT * FROM Usuarios WHERE ID = :user_id"), {'user_id': user_id}).fetchone()
        if user_data:
            return User(
                user_data.ID,
                user_data.Nome,
                user_data.Sobrenome,
                user_data.Funcao,
                user_data.Login,
                user_data.FotoUsuarioURI
            )
        return None


engine = create_engine(
    'mysql://root:#teste123321@localhost:3306/Biblioteca'
)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/perform_login', methods=['POST'])
def perform_login():
    login = request.form.get('login')
    senha = request.form.get('senha')
    user_data = db.session.execute(text(
        "SELECT * FROM Usuarios WHERE Login = :login"), {'login': login}).fetchone()
    if user_data and check_password_hash(user_data.SenhaCriptografada, senha):
        user = User(
            user_id=user_data.ID,
            login=user_data.Login,
            sobrenome=user_data.Sobrenome,
            funcao=user_data.Funcao,
            foto_usuario_uri=user_data.FotoUsuarioURI
        )
        login_user(user)
        return redirect(url_for('index'))
    else:
        return render_template('login.html', error="Login ou senha incorretos")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/registrar')
def registrar():
    return render_template('registrar.html')


@app.route('/add_livro', methods=['GET', 'POST'])
@login_required
def add_livro():
    mensagem = None
    if current_user.funcao != 'aluno':
        if request.method == 'POST':
            isbn = request.form['isbn']
            titulo = request.form['titulo']
            autor = request.form['autor']
            descricao = request.form['descricao']
            categoria = request.form['categoria']
            data_aquisicao = datetime.strptime(
                request.form['data_aquisicao'], '%Y-%m-%d').date()
            estado_conservacao = request.form['estado_conservacao']
            localizacao_fisica = request.form['localizacao_fisica']
            capa_livro_uri = request.form['capa_livro_uri']

            sql = text("""INSERT INTO Livros (ISBN, Titulo, Autor, Descricao, Categoria, DataAquisicao, EstadoConservacao, LocalizacaoFisica, CapaLivroURI) 
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
                mensagem = {'conteudo': 'Livro adicionado com sucesso!',
                            'classe': 'mensagem-sucesso'}
            except Exception as e:
                db.session.rollback()
                mensagem = {
                    'conteudo': f'Erro ao adicionar o livro: {str(e)}', 'classe': 'mensagem-erro'}

    return render_template('cadastrar_livro.html', mensagem=mensagem)


@app.route('/update_livro', methods=['GET', 'POST'])
@login_required
def update_livro():
    mensagem = None
    livro = None
    if current_user.funcao != 'aluno':
        if request.method == 'POST':
            isbn_pesquisa = request.form.get('isbn_pesquisa')

            # Certifique-se de que ISBN não seja None antes de fazer a consulta
            if isbn_pesquisa is not None:
                livro = db.session.execute(text(
                    "SELECT * FROM livros WHERE ISBN = :isbn"), {'isbn': isbn_pesquisa}).fetchone()

            if livro:
                return redirect(url_for('update_livro_form', isbn=isbn_pesquisa))
            else:
                mensagem = {'conteudo': 'Livro não encontrado.',
                            'classe': 'mensagem-erro'}

    return render_template('update_livro_pesquisa.html', mensagem=mensagem)


@app.route('/update_livro/<isbn>', methods=['GET', 'POST'])
@login_required
def update_livro_form(isbn):
    livro = db.session.execute(
        text("SELECT * FROM livros WHERE ISBN = :isbn"), {'isbn': isbn}).fetchone()
    mensagem = None
    if current_user.funcao != 'aluno':
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
@login_required
def delete_livro():
    mensagem = None
    livro = None
    if current_user.funcao != 'aluno':
        if request.method == 'POST':
            isbn = request.form.get('isbn')
            livro = db.session.execute(
                text("SELECT * FROM livros WHERE ISBN = :isbn"), {'isbn': isbn}).fetchone()

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
@login_required
def add_material():
    mensagem = None
    if current_user.funcao != 'aluno':
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

            try:
                db.session.execute(sql)
                db.session.commit()
                mensagem = {
                    'conteudo': 'Material didático adicionado com sucesso!', 'classe': 'mensagem-sucesso'}
            except Exception as e:
                db.session.rollback()
                mensagem = {
                    'conteudo': f'Erro ao adicionar o material didático: {str(e)}', 'classe': 'mensagem-erro'}

    return render_template('cadastrar_material.html', mensagem=mensagem)


@app.route('/update_material', methods=['GET', 'POST'])
@login_required
def update_material():
    mensagem = None
    material = None
    if current_user.funcao != 'aluno':
        if request.method == 'POST':
            id_pesquisa = request.form.get('id_pesquisa')
            # Certifique-se de que ID não seja None antes de fazer a consulta
            if id_pesquisa is not None:
                material = db.session.execute(text(
                    "SELECT * FROM materiaisdidaticos WHERE ID = :id"), {'id': id_pesquisa}).fetchone()

            if material:
                return redirect(url_for('update_material_form', id=id_pesquisa))
            else:
                mensagem = {
                    'conteudo': 'Material didático não encontrado.', 'classe': 'mensagem-erro'}

        return render_template('update_material_pesquisa.html', mensagem=mensagem)


@app.route('/update_material/<id>', methods=['GET', 'POST'])
@login_required
def update_material_form(id):
    material = db.session.execute(
        text("SELECT * FROM materiaisdidaticos WHERE ID = :id"), {'id': id}).fetchone()
    mensagem = None
    if current_user.funcao != 'aluno':
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
                    mensagem = {
                        'conteudo': 'Material didático atualizado com sucesso!', 'classe': 'mensagem-sucesso'}
                except Exception as e:
                    db.session.rollback()
                    mensagem = {
                        'conteudo': f'Erro ao atualizar o material didático: {str(e)}', 'classe': 'mensagem-erro'}
            else:
                mensagem = {
                    'conteudo': 'Material didático não encontrado para atualização.', 'classe': 'mensagem-erro'}

    return render_template('update_material.html', material=material, mensagem=mensagem)


@app.route('/delete_material', methods=['GET', 'POST'])
@login_required
def delete_material():
    mensagem = None
    material = None
    if current_user.funcao != 'aluno':
        if request.method == 'POST':
            id = request.form.get('id')
            material = db.session.execute(
                text("SELECT * FROM materiaisdidaticos WHERE ID = :id"), {'id': id}).fetchone()

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

@app.route('/usuarios_crud')
def usuarios_crud():
    return render_template('usuarios_crud.html')

@app.route('/add_usuario', methods=['POST'])
def add_usuario():
    try:
        if request.method == 'POST':
            nome = request.form['nome']
            sobrenome = request.form['sobrenome']
            login = request.form['login']
            senha = request.form['senha']
            tipo = request.form['tipo']
            foto = request.form['foto']

            funcao = tipo

            db.session.execute(text("""
                INSERT INTO Usuarios (Nome, Sobrenome, Funcao, Login, SenhaCriptografada, FotoUsuarioURI)
                VALUES (:nome, :sobrenome, :funcao, :login, :senha, :foto)
            """), {
                'nome': nome,
                'sobrenome': sobrenome,
                'funcao': funcao,
                'login': login,
                'senha': generate_password_hash(senha, method='sha256'),
                'foto': foto
            })

            db.session.commit()
            return 'Usuário adicionado com sucesso!'
    except Exception as e:
        db.session.rollback()
        return f'Erro ao adicionar usuário: {str(e)}'


@app.route('/update_usuario', methods=['GET', 'POST'])
def update_usuario():
    mensagem = None

    if request.method == 'POST':
        user_id = request.form.get('user_id')

        sql_user = text("SELECT ID FROM usuarios WHERE usuarios.ID = :user_id")
        id_user = db.session.execute(sql_user, {'user_id': user_id}).first()

        if id_user is not None:
            return redirect(url_for('update_usuario_form', id=id_user[0]))
        else:
            mensagem = {'conteudo': 'Usuário não encontrado.', 'classe': 'mensagem-erro'}

    return render_template('update_usuario.html', mensagem=mensagem)


@app.route('/update_usuario_form/<id>', methods=['GET', 'POST'])
def update_usuario_form(id):
    mensagem = None

    sql = text("SELECT * FROM usuarios WHERE ID = :user_id")
    usuario = db.session.execute(sql, {'user_id': id}).first()

    if usuario is None:
        mensagem = {'conteudo': 'Usuário não encontrado.', 'classe': 'mensagem-erro'}
    elif request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        funcao = request.form['funcao']
        login = request.form['login']
        senha = request.form['senha']
        foto = request.form['foto']

        update_sql = text("""
            UPDATE usuarios
            SET Nome = :nome,
                Sobrenome = :sobrenome,
                Funcao = :funcao,
                Login = :login,
                SenhaCriptografada = :senha,
                FotoUsuarioURI = :foto
            WHERE ID = :user_id
        """)

        try:
            db.session.execute(update_sql, {'nome': nome, 'sobrenome': sobrenome, 'funcao': funcao,
                                            'login': login, 'senha': senha, 'foto': foto, 'user_id': id})
            db.session.commit()
            mensagem = {'conteudo': 'Usuário atualizado com sucesso!', 'classe': 'mensagem-sucesso'}
        except Exception as e:
            db.session.rollback()
            mensagem = {'conteudo': f'Erro ao atualizar usuário: {str(e)}', 'classe': 'mensagem-erro'}

    return render_template('update_usuario_pesquisa.html', usuario=usuario, mensagem=mensagem)



@app.route('/delete_usuario', methods=['POST'])
@login_required
def delete_usuario():
    mensagem = None
    usuario = None
    if current_user.funcao != 'aluno':
        if request.method == 'POST':
            id_usuario_a_excluir = request.form.get('id')
            usuario = db.session.execute(
                text("SELECT * FROM usuarios WHERE ID = :id"), {'id': id_usuario_a_excluir}).fetchone()

            if usuario:
                sql = text("DELETE FROM usuarios WHERE ID = :id")

                try:
                    db.session.execute(sql, {'id': id_usuario_a_excluir})
                    db.session.commit()
                    mensagem = {
                        'conteudo': 'Usuário excluído com sucesso!', 'classe': 'mensagem-sucesso'}
                except Exception as e:
                    db.session.rollback()
                    mensagem = {
                        'conteudo': f'Erro ao excluir o usuário: {str(e)}', 'classe': 'mensagem-erro'}
            else:
                mensagem = {
                    'conteudo': 'Usuário não encontrado para exclusão.', 'classe': 'mensagem-erro'}

    return render_template('delete_usuario.html', usuario=usuario, mensagem=mensagem)


@app.route('/get_usuario/<id>')
def get_usuario(id):
    user = db.session.execute(
        text("SELECT * FROM usuarios WHERE ID = :id"), {'id': id}).fetchone()

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


@app.route('/get_usuarios')
def get_usuarios():
    sql = text(
        """SELECT Nome, Sobrenome, Funcao FROM Usuarios"""
    )

    usuarios = db.session.execute(sql).fetchall()

    usuarios_json = [{'Nome': usuario.Nome, 'Sobrenome': usuario.Sobrenome, 'Funcao': usuario.Funcao} for usuario in usuarios]

    return jsonify(usuarios_json)


# Emprestimos ---------------------------------------------


@app.route('/add_emprestimo', methods=['GET', 'POST'])
def add_emprestimo():
    mensagem = None
    if request.method == 'POST':
        name = request.form['user']
        isbn = request.form['book']
        material = request.form['material']
        data_emp = request.form['data_emprestimo']
        data_dev = request.form['data_devolucao']
        # status = request.form['status']
        sql_user = text(
            """SELECT ID FROM Usuarios WHERE Usuarios.Nome = '{name}'""".format(name=name))
        sql_book = text(
            """SELECT ISBN FROM Livros WHERE Livros.ISBN = '{isbn}'""".format(isbn=isbn))
        id_user = db.session.execute(sql_user)
        id_book = db.session.execute(sql_book)
        user_tuple = id_user.first()
        book_tuple = id_book.first()
        if user_tuple and book_tuple is not None:
            sql = text(
                """INSERT INTO Emprestimos (IDUsuario, IDLivro, IDMaterialDidatico, DataEmprestimo, DataDevolucaoPrevista) 
            VALUES ({user}, {livro}, {material}, '{data_emp}', '{data_dev}');""".format(
                    user=user_tuple[0], livro=book_tuple[0], material=material, data_emp=data_emp, data_dev=data_dev))
            try:
                db.session.execute(sql)
                mensagem = {'conteudo': 'Emprestimo adicionado com sucesso!',
                            'classe': 'mensagem-sucesso'}
            except Exception as e:
                mensagem = {
                    'conteudo': f'Erro ao adicionar o livro: {str(e)}', 'classe': 'mensagem-erro'}
        else:
            mensagem = {
                'conteudo': f'Erro ao adicionar o livro', 'classe': 'mensagem-erro'}

    return render_template('cadastrar_emprestimo.html', mensagem=mensagem)


@app.route('/update_emprestimo', methods=['GET', 'POST'])
def update_emprestimo():
    mensagem = None
    emprestimo = None

    if request.method == 'POST':
        name = request.form.get('name')
        isbn = request.form.get('isbn')

        sql_user = text(
            """SELECT ID FROM Usuarios WHERE Usuarios.Nome = '{name}'""".format(name=name))
        sql_book = text(
            """SELECT ISBN FROM Livros WHERE Livros.ISBN = '{isbn}'""".format(isbn=isbn))
        id_user = db.session.execute(sql_user)
        id_book = db.session.execute(sql_book)
        user_tuple = id_user.first()
        book_tuple = id_book.first()
        if user_tuple and book_tuple is not None:
            sql = text(
                """SELECT * FROM Emprestimos AS E WHERE E.IDUsuario = {id_user} AND E.IDLivro = {id_book} """.format(id_user=user_tuple[0], id_book=book_tuple[0]))
            emprestimo = db.session.execute(sql).first()

            if emprestimo:
                return redirect(url_for('update_emprestimo_form', id=emprestimo[0]))
            else:
                mensagem = {'conteudo': 'emprestimo não encontrado.',
                            'classe': 'mensagem-erro'}
        else:
            mensagem = {'conteudo': 'emprestimo não encontrado.',
                        'classe': 'mensagem-erro'}

    return render_template('update_emprestimo_pesquisa.html', mensagem=mensagem)


@app.route('/update_emprestimo_form/<id>', methods=['GET', 'POST'])
def update_emprestimo_form(id):
    mensagem = None
    sql = text(
        """SELECT * FROM Emprestimos AS E WHERE E.ID = {emp_id}""".format(emp_id=id))
    emprestimo = db.session.execute(sql).first()
    if request.method == 'POST':
        data_emp = request.form['data_emprestimo']
        data_dev = request.form['data_devolucao']
        sql = text(
            """UPDATE Emprestimos SET DataEmprestimo = '{data_emp}', 
            DataDevolucaoPrevista = '{data_dev}' WHERE ID = {emp_id};""".format(
                data_emp=data_emp, data_dev=data_dev, emp_id=id))
        try:
            db.session.execute(sql)
            mensagem = {'conteudo': 'Emprestimo atualizado com sucesso!',
                        'classe': 'mensagem-sucesso'}
        except Exception as e:
            db.session.rollback()
            mensagem = {
                'conteudo': f'Erro ao atualizar emprestimo: {str(e)}', 'classe': 'mensagem-erro'}

    return render_template('update_emprestimo_form.html', emprestimo=emprestimo, mensagem=mensagem)


@app.route('/get_emprestimos_estudante/<id>')
def get_emprestimos_estudante(id):
    emprestimos = []
    sql = text(
        """SELECT * FROM Emprestimos AS E WHERE E.IDUsuario = {id_user}""".format(id_user=id))
    result = db.session.execute(sql)
    for row in db.session.execute(sql):
        emprestimos.append(emprestimo_module.initialize(row))

    return emprestimos


@app.route('/delete_emprestimo', methods=['GET', 'POST'])
def delete_emprestimo():
    mensagem = None
    emprestimo = None

    if request.method == 'POST':
        name = request.form.get('name')
        isbn = request.form.get('isbn')

        sql_user = text(
            """SELECT ID FROM Usuarios WHERE Usuarios.Nome = '{name}'""".format(name=name))
        sql_book = text(
            """SELECT ISBN FROM Livros WHERE Livros.ISBN = '{isbn}'""".format(isbn=isbn))
        id_user = db.session.execute(sql_user).first()[0]
        id_book = db.session.execute(sql_book).first()[0]

        if name and isbn is not None:
            try:
                sql = text(
                    """DELETE FROM Emprestimos WHERE IDUsuario = {id_user} AND IDLivro = {id_book} """.format(id_user=id_user, id_book=id_book))
                db.session.execute(sql)
                mensagem = {'conteudo': 'Livro excluído com sucesso!',
                            'classe': 'mensagem-sucesso'}
            except Exception as e:
                db.session.rollback()
                mensagem = {
                    'conteudo': f'Erro ao excluir o livro: {str(e)}', 'classe': 'mensagem-erro'}
    return render_template('delete_emprestimo.html', mensagem=mensagem)


@app.route('/get_emprestimo', methods=['GET', 'POST'])
def get_emprestimo():
    mensagem = None
    emprestimo = None

    if request.method == 'POST':
        name = request.form.get('name')
        isbn = request.form.get('isbn')

        sql_user = text(
            """SELECT ID FROM Usuarios WHERE Usuarios.Nome = '{name}'""".format(name=name))
        sql_book = text(
            """SELECT ISBN FROM Livros WHERE Livros.ISBN = '{isbn}'""".format(isbn=isbn))
        id_user = db.session.execute(sql_user)
        id_book = db.session.execute(sql_book)

        if id_user and id_book.first is not None:
            sql = text(
                """SELECT * FROM Emprestimos AS E WHERE E.IDUsuario = {id_user} AND E.IDLivro = {id_book} """.format(id_user=id_user.first()[0], id_book=id_book.first()[0]))
            emprestimo = db.session.execute(sql).first()

            if emprestimo:
                return emprestimo_module.initialize(emprestimo)
            else:
                mensagem = {'conteudo': 'emprestimo não encontrado.',
                            'classe': 'mensagem-erro'}
        else:
            mensagem = {'conteudo': 'emprestimo não encontrado.',
                        'classe': 'mensagem-erro'}

    return render_template('get_emprestimo.html', mensagem=mensagem)


@app.route('/emprestimos_crud')
def emprestimos_crud():
        if current_user.funcao != 'aluno':
            return render_template('emprestimos_crud.html')
        else:
            return render_template('emprestimos_crud.html', link='/get_emprestimos_estudante/{id_user}'.format(id_user=current_user.id))


if __name__ == '__main__':
    app.run(debug=True)
