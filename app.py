from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Livros, MaterialDidatico, Usuario, Emprestimo
from datetime import datetime
from sqlalchemy import text
from sqlalchemy import create_engine
import json

app = Flask(__name__)
# COLOQUE A URL DO SEU BANCO NA LINHA 9, AINDA NÃO ESTÁ INTEGRADO
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://lucas:password@localhost:3306/Test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chave'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_PASSWORD'] = 'password'

db.init_app(app)

engine = create_engine(
    'mysql://lucas:password@localhost:3306/Test'
)


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
        data_aquisicao = datetime.strptime(
            request.form['data_aquisicao'], '%Y-%m-%d').date()
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
            mensagem = {'conteudo': 'Livro adicionado com sucesso!',
                        'classe': 'mensagem-sucesso'}
        except Exception as e:
            db.session.rollback()
            mensagem = {
                'conteudo': f'Erro ao adicionar o livro: {str(e)}', 'classe': 'mensagem-erro'}

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
            mensagem = {'conteudo': 'Livro não encontrado.',
                        'classe': 'mensagem-erro'}

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
            livro.DataAquisicao = datetime.strptime(
                data.get('data_aquisicao', str(livro.DataAquisicao)), '%Y-%m-%d').date()
            livro.EstadoConservacao = data.get(
                'estado_conservacao', livro.EstadoConservacao)
            livro.LocalizacaoFisica = data.get(
                'localizacao_fisica', livro.LocalizacaoFisica)
            livro.CapaLivroURI = data.get('capa_livro_uri', livro.CapaLivroURI)

            try:
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
        livro = Livros.query.get(isbn)

        if livro:
            try:
                db.session.delete(livro)
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
    sql = text("SELECT ISBN FROM livros")
    livros_json = [{'ISBN': livro.ISBN, 'Titulo': livro.Titulo,
                    'Autor': livro.Autor} for livro in livros]
    data = engine.execute(sql)
    for row in data:
        print(row)
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
            mensagem = {
                'conteudo': 'Material didático adicionado com sucesso!', 'classe': 'mensagem-sucesso'}
        except Exception as e:
            db.session.rollback()
            mensagem = {
                'conteudo': f'Erro ao adicionar o material didático: {str(e)}', 'classe': 'mensagem-erro'}

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
            mensagem = {
                'conteudo': 'Material didático não encontrado.', 'classe': 'mensagem-erro'}

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
            material.NumeroSerie = data.get(
                'numero_serie', material.NumeroSerie)
            material.EstadoConservacao = data.get(
                'estado_conservacao', material.EstadoConservacao)
            material.LocalizacaoFisica = data.get(
                'localizacao_fisica', material.LocalizacaoFisica)
            material.FotoMaterialURI = data.get(
                'foto_material_uri', material.FotoMaterialURI)

            try:
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
    materiais_json = [{'ID': material.ID, 'Descricao': material.Descricao,
                       'Categoria': material.Categoria} for material in materiais]
    return jsonify(materiais_json)


@app.route('/materiais_crud')
def materiais_crud():
    return render_template('material_crud.html')

# Usuarios ---------------------------------------------------


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


@app.route('/delete_usuario/<id>', methods=['DELETE'])
def delete_usuario(id):
    user = Usuario.query.get(id)
    if user is None:
        return jsonify({'error': 'Usuario não encontrado'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuario excluído com sucesso'}), 200


@app.route('/get_usuario/<id>')
def get_usuario(id):
    user = Usuario.query.get(id)
    if user is None:
        return jsonify({'error': 'Material não encontrado'}), 404

    user_json = {
        'Nome': user.Nome,
        'Sobrenome': user.Sobrenome,
        'Funcao': user.Funcao,
        'Login': user.Login,
        'SenhaCriptografada': user.SenhaCriptografada,
        'user.FotoUsuarioURI': user.FotoUsuarioURI
    }

    return jsonify(user_json)

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
