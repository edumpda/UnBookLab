from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Livros, MaterialDidatico, Usuario, Emprestimo
from datetime import datetime
import json

app = Flask(__name__)
<<<<<<< Updated upstream
# COLOQUE A URL DO SEU BANCO NA LINHA 9, AINDA NÃO ESTÁ INTEGRADO
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:lucasql@localhost:3306/biblioteca'
=======

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:lucasql@localhost:3306/Biblioteca'
>>>>>>> Stashed changes
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chave'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_PASSWORD'] = 'password'

db.init_app(app)

<<<<<<< Updated upstream
=======
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user_data = db.session.execute(text("SELECT * FROM usuarios WHERE ID = :user_id"), {'user_id': user_id}).fetchone()
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
        user_data = db.session.execute(text("SELECT * FROM Usuarios WHERE ID = :user_id"), {'user_id': user_id}).fetchone()
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
    'mysql://root:lucasql@localhost:3306/Biblioteca'
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

>>>>>>> Stashed changes

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_db')
def create_db():
    db.create_all()
    return 'Banco de dados criado'


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

        livro = Livros(
            ISBN=isbn,
            Titulo=titulo,
            Autor=autor,
            Descricao=descricao,
            Categoria=categoria,
            DataAquisicao=data_aquisicao,
            EstadoConservacao=estado_conservacao,
            LocalizacaoFisica=localizacao_fisica,
            CapaLivroURI=capa_livro_uri
        )
        try:
            db.session.add(livro)
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
        app.logger.info(f"Formulário Recebido: {request.form}")
        print(f"Conteúdo do Formulário: {request.form}")
        print(f"ISBN Pesquisado: {isbn_pesquisa}")

        # Certifique-se de que ISBN não seja None antes de fazer a consulta
        if isbn_pesquisa is not None:
            livro = Livros.query.get(isbn_pesquisa)

        if livro:
            return redirect(url_for('update_livro_form', isbn=isbn_pesquisa))
        else:
            mensagem = {'conteudo': 'Livro não encontrado.', 'classe': 'mensagem-erro'}

    return render_template('update_livro_pesquisa.html', mensagem=mensagem)


@app.route('/update_livro/<isbn>', methods=['GET', 'POST'])
def update_livro_form(isbn):
    livro = Livros.query.get(isbn)
    mensagem = None

    if request.method == 'POST':
        if livro:
            data = request.form
            livro.Titulo = data.get('titulo', livro.Titulo)
            livro.Autor = data.get('autor', livro.Autor)
            livro.Descricao = data.get('descricao', livro.Descricao)
            livro.Categoria = data.get('categoria', livro.Categoria)
            livro.DataAquisicao = datetime.strptime(data.get('data_aquisicao', str(livro.DataAquisicao)), '%Y-%m-%d').date()
            livro.EstadoConservacao = data.get('estado_conservacao', livro.EstadoConservacao)
            livro.LocalizacaoFisica = data.get('localizacao_fisica', livro.LocalizacaoFisica)
            livro.CapaLivroURI = data.get('capa_livro_uri', livro.CapaLivroURI)

            try:
                db.session.commit()
                mensagem = {'conteudo': 'Livro atualizado com sucesso!', 'classe': 'mensagem-sucesso'}
            except Exception as e:
                db.session.rollback()
                mensagem = {'conteudo': f'Erro ao atualizar o livro: {str(e)}', 'classe': 'mensagem-erro'}
        else:
            mensagem = {'conteudo': 'Livro não encontrado para atualização.', 'classe': 'mensagem-erro'}
    
    return render_template('update_livro.html', livro=livro, mensagem=mensagem)




@app.route('/delete_livro', methods=['GET', 'POST'])
def delete_livro():
    mensagem = None
    livro = None

    if request.method == 'POST':
        isbn = request.form.get('isbn')
        livro = Livros.query.get(isbn)

        if livro:
            try:
                db.session.delete(livro)
                db.session.commit()
                mensagem = {'conteudo': 'Livro excluído com sucesso!', 'classe': 'mensagem-sucesso'}
            except Exception as e:
                db.session.rollback()
                mensagem = {'conteudo': f'Erro ao excluir o livro: {str(e)}', 'classe': 'mensagem-erro'}
        else:
            mensagem = {'conteudo': 'Livro não encontrado para exclusão.', 'classe': 'mensagem-erro'}

    return render_template('delete_livro.html', livro=livro, mensagem=mensagem)


@app.route('/get_livro', methods=['GET', 'POST'])
def get_livro():
    if request.method == 'POST':
        isbn = request.form.get('isbn')

        if not isbn:
            return jsonify({'error': 'ISBN não fornecido'}), 400

        livro = Livros.query.get(isbn)

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
    livros = Livros.query.all()
    livros_json = [{'ISBN': livro.ISBN, 'Titulo': livro.Titulo, 'Autor': livro.Autor} for livro in livros]
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

        material = MaterialDidatico(
            Descricao=descricao,
            Categoria=categoria,
            NumeroSerie=numero_serie,
            EstadoConservacao=estado_conservacao,
            LocalizacaoFisica=localizacao_fisica,
            FotoMaterialURI=foto_material_uri
        )
        try:
            db.session.add(material)
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
            material = MaterialDidatico.query.get(id_pesquisa)

        if material:
            return redirect(url_for('update_material_form', id=id_pesquisa))
        else:
            mensagem = {'conteudo': 'Material didático não encontrado.', 'classe': 'mensagem-erro'}

    return render_template('update_material_pesquisa.html', mensagem=mensagem)


@app.route('/update_material/<id>', methods=['GET', 'POST'])
def update_material_form(id):
    material = MaterialDidatico.query.get(id)
    mensagem = None

    if request.method == 'POST':
        if material:
            data = request.form
            material.Descricao = data.get('descricao', material.Descricao)
            material.Categoria = data.get('categoria', material.Categoria)
            material.NumeroSerie = data.get('numero_serie', material.NumeroSerie)
            material.EstadoConservacao = data.get('estado_conservacao', material.EstadoConservacao)
            material.LocalizacaoFisica = data.get('localizacao_fisica', material.LocalizacaoFisica)
            material.FotoMaterialURI = data.get('foto_material_uri', material.FotoMaterialURI)

            try:
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
        material = MaterialDidatico.query.get(id)

        if material:
            try:
                db.session.delete(material)
                db.session.commit()
                mensagem = {'conteudo': 'Material didático excluído com sucesso!', 'classe': 'mensagem-sucesso'}
            except Exception as e:
                db.session.rollback()
                mensagem = {'conteudo': f'Erro ao excluir o material didático: {str(e)}', 'classe': 'mensagem-erro'}
        else:
            mensagem = {'conteudo': 'Material didático não encontrado para exclusão.', 'classe': 'mensagem-erro'}

    return render_template('delete_material.html', material=material, mensagem=mensagem)


@app.route('/get_material', methods=['GET', 'POST'])
def get_material():
    if request.method == 'POST':
        id = request.form.get('id')

        if not id:
            return jsonify({'error': 'ID não fornecido'}), 400

        material = MaterialDidatico.query.get(id)

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
    materiais = MaterialDidatico.query.all()
    materiais_json = [{'ID': material.ID, 'Descricao': material.Descricao, 'Categoria': material.Categoria} for material in materiais]
    return jsonify(materiais_json)


@app.route('/materiais_crud')
def materiais_crud():
    return render_template('material_crud.html')

# Usuarios ---------------------------------------------------

@app.route('/usuarios_crud')
def usuarios_crud():
    # Lógica para a página de CRUD de usuários
    return render_template('usuarios_crud.html')

<<<<<<< Updated upstream
@app.route('/add_usuario')
def add_usuario():
    user = Usuario(
        Nome='name',
        Sobrenome='last name',
        Funcao='function',
        Login='login',
        SenhaCriptografada='password',
        FotoUsuarioURI='photo'
    )
    db.session.add(user)
    db.session.commit()
    return 'user add'


@app.route('/update_usuario/<id>', methods=['PUT'])
def update_usuario(id):
    user = Usuario.query.get(id)
    if user is None:
        return jsonify({'error': 'Usuario não encontrado'}), 404

    data = request.json
    user.Nome = data.get('Nome', user.Nome)
    user.Sobrenome = data.get('Sobrenome', user.Sobrenome)
    user.Funcao = data.get('Funcao', user.Funcao)
    user.Login = data.get('Login', user.Login)
    user.SenhaCriptografada = data.get(
        'SenhaCriptografada', user.SenhaCriptografada)
    user.FotoUsuarioURI = data.get('FotoUsuarioURI', user.FotoUsuarioURI)

    db.session.commit()
    return jsonify({'message': 'Usuario atualizado com sucesso'}), 200
=======
@app.route('/add_usuario', methods=['GET', 'POST'])
def add_usuario():
    # Lógica para a página de cadastro de usuários
    mensagem = None
    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        login = request.form['login']
        senha = request.form['senha']
        tipo = request.form['tipo']
        foto = request.form['foto']

        funcao = tipo

        sql = text("""
            INSERT INTO Usuarios (Nome, Sobrenome, Funcao, Login, SenhaCriptografada, FotoUsuarioURI)
            VALUES (:nome, :sobrenome, :funcao, :login, :senha, :foto)
        """)

        try:
            db.session.execute(sql, {
                'nome': nome,
                'sobrenome': sobrenome,
                'funcao': funcao,
                'login': login,
                'senha': generate_password_hash(senha, method='pbkdf2:sha256'),
                'foto': foto
            })

            db.session.commit()
            mensagem = {'conteudo': 'Usuário adicionado com sucesso!',
                        'classe': 'mensagem-sucesso'}
        except Exception as e:
            db.session.rollback()
            mensagem = {
                'conteudo': f'Erro ao adicionar usuário: {str(e)}', 'classe': 'mensagem-erro'}

    return render_template('registar.html', mensagem=mensagem)

@app.route('/update_usuario', methods=['GET', 'POST'])
def update_usuario():
    mensagem = None
    usuario = None

    if request.method == 'POST':
        # Assuming you have a form with appropriate fields for user updates
        # Adjust the form field names as needed
        user_id = request.form.get('user_id')
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        funcao = request.form.get('funcao')
        login = request.form.get('login')
        senha = request.form.get('senha')
        foto = request.form.get('foto')

        sql_user = text(
            """SELECT ID FROM usuarios WHERE usuarios.ID = '{user_id}'""".format(user_id=user_id))
        id_user = db.session.execute(sql_user)
        user_tuple = id_user.first()

        if user_tuple is not None:
            sql = text("""
                SELECT * FROM usuarios WHERE ID = {user_id}
            """.format(user_id=user_tuple[0]))

            usuario = db.session.execute(sql).first()

            if usuario:
                return redirect(url_for('update_usuario_form', id=usuario[0]))
            else:
                mensagem = {'conteudo': 'Usuário não encontrado.',
                            'classe': 'mensagem-erro'}
        else:
            mensagem = {'conteudo': 'Usuário não encontrado.',
                        'classe': 'mensagem-erro'}

    return render_template('update_usuario.html', mensagem=mensagem)


@app.route('/update_usuario_form/<id>', methods=['GET', 'POST'])
def update_usuario_form(id):
    mensagem = None
    sql = text(
        """SELECT * FROM usuarios WHERE ID = {user_id}""".format(user_id=id))
    usuario = db.session.execute(sql).first()

    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        funcao = request.form['funcao']
        login = request.form['login']
        senha = request.form['senha']
        foto = request.form['foto']

        sql = text("""
            UPDATE usuarios
            SET Nome = '{nome}',
                Sobrenome = '{sobrenome}',
                Funcao = '{funcao}',
                Login = '{login}',
                SenhaCriptografada = '{senha}',
                FotoUsuarioURI = '{foto}'
            WHERE ID = {user_id}
        """.format(
            nome=nome, sobrenome=sobrenome, funcao=funcao, login=login, senha=senha, foto=foto, user_id=id))

        try:
            db.session.execute(sql)
            mensagem = {'conteudo': 'Usuário atualizado com sucesso!',
                        'classe': 'mensagem-sucesso'}
        except Exception as e:
            db.session.rollback()
            mensagem = {
                'conteudo': f'Erro ao atualizar usuário: {str(e)}', 'classe': 'mensagem-erro'}

    return render_template('update_usuario.html', usuario=usuario, mensagem=mensagem)

>>>>>>> Stashed changes


@app.route('/delete_usuario/<id>', methods=['DELETE'])
def delete_usuario(id):
    user = Usuario.query.get(id)
    if user is None:
        return jsonify({'error': 'Usuario não encontrado'}), 404

<<<<<<< Updated upstream
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuario excluído com sucesso'}), 200
=======
    if user_existente:
        try:
            db.session.execute(
                text("DELETE FROM usuarios WHERE ID = :id"), {'id': id})
            db.session.commit()
            return jsonify({'message': 'Usuário excluído com sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Erro ao excluir o usuário: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Usuário não encontrado'}), 404
>>>>>>> Stashed changes

# Example of generating URL for the delete_usuario endpoint
# Make sure to replace 'user_id' with the actual ID of the user you want to delete
url = url_for('delete_usuario', id=user_id)


@app.route('/get_usuario/<id>')
def get_usuario(id):
    user = Usuario.query.get(id)
    if user is None:
        return jsonify({'error': 'Material não encontrado'}), 404

<<<<<<< Updated upstream
    user_json = {
        'Nome': user.Nome,
        'Sobrenome': user.Sobrenome,
        'Funcao': user.Funcao,
        'Login': user.Login,
        'SenhaCriptografada': user.SenhaCriptografada,
        'user.FotoUsuarioURI': user.FotoUsuarioURI
    }
=======
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
>>>>>>> Stashed changes

    return jsonify(user_json)


# Emprestimos ---------------------------------------------


@app.route('/add_emprestimo')
def add_emprestimo():
    emprestimo = Emprestimo(
        IDUsuario=Usuario.query.first().ID,
        IDLivro=Livros.query.first().ISBN,
        IDMaterialDidatico=MaterialDidatico.query.first().ID,
        DataEmprestimo="2017-01-01",
        DataDevolucaoPrevista="2017-01-01",
        Status="dshfjdfshj",
    )
    db.session.add(emprestimo)
    db.session.commit()
    return 'emprestimo add'


@app.route('/update_emprestimo/<id>', methods=['PUT'])
def update_emprestimo(id):
    emprestimo = Emprestimo.query.get(id)
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
    emprestimo = Emprestimo.query.get(id)
    if emprestimo is None:
        return jsonify({'error': 'Emprestimo não encontrado'}), 404

    db.session.delete(emprestimo)
    db.session.commit()
    return jsonify({'message': 'Emprestimo excluído com sucesso'}), 200


@app.route('/get_emprestimo/<id>')
def get_emprestimo(id):
    emprestimo = Emprestimo.query.get(id)
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

