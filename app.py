from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Livros, MaterialDidatico, Usuario, Emprestimo
from datetime import datetime
import json

app = Flask(__name__)
# COLOQUE A URL DO SEU BANCO NA LINHA 9, AINDA NÃO ESTÁ INTEGRADO
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:#teste123321@localhost:3306/Biblioteca'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chave'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_PASSWORD'] = 'password'

db.init_app(app)


@app.route('/')
def index():
    return 'Hello World'


@app.route('/create_db')
def create_db():
    db.create_all()
    return 'Banco de dados criado'


@app.route('/add_livro')
def add_livro():
    livro = Livros(ISBN='9788575221631', Titulo='Guia Mangá de Bancos de Dados', Autor='Mana Takahashi', Descricao='Descrição grande demais', Categoria='Educação', DataAquisicao=datetime.strptime(
        '2023-11-19', '%Y-%m-%d').date(), EstadoConservacao='Novo', LocalizacaoFisica='Estante 1', CapaLivroURI='https://s3-sa-east-1.amazonaws.com/catalogodasartes/obra_13269947.jpg')
    db.session.add(livro)
    db.session.commit()
    return 'Livro adicionado'


@app.route('/update_livro/<isbn>', methods=['PUT'])
def update_livro(isbn):
    livro = Livros.query.get(isbn)
    if livro is None:
        return jsonify({'error': 'Livro não encontrado'}), 404

    data = request.json
    livro.Titulo = data.get('Titulo', livro.Titulo)
    livro.Autor = data.get('Autor', livro.Autor)
    livro.Descricao = data.get('Descricao', livro.Descricao)
    livro.Categoria = data.get('Categoria', livro.Categoria)
    data_aquisicao = data.get('DataAquisicao', str(livro.DataAquisicao))
    livro.DataAquisicao = datetime.strptime(data_aquisicao, '%Y-%m-%d').date()
    livro.EstadoConservacao = data.get(
        'EstadoConservacao', livro.EstadoConservacao)
    livro.LocalizacaoFisica = data.get(
        'LocalizacaoFisica', livro.LocalizacaoFisica)
    livro.CapaLivroURI = data.get('CapaLivroURI', livro.CapaLivroURI)

    db.session.commit()
    return jsonify({'message': 'Livro atualizado com sucesso'}), 200


@app.route('/delete_livro/<isbn>', methods=['DELETE'])
def delete_livro(isbn):
    livro = Livros.query.get(isbn)
    if livro is None:
        return jsonify({'error': 'Livro não encontrado'}), 404

    db.session.delete(livro)
    db.session.commit()
    return jsonify({'message': 'Livro excluído com sucesso'}), 200


@app.route('/get_livro/<isbn>')
def get_livro(isbn):
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


@app.route('/get_livros')
def get_livros():
    from models import Livros

    livros = Livros.query.all()
    livros_json = [{'ISBN': livro.ISBN, 'Titulo': livro.Titulo,
                    'Autor': livro.Autor} for livro in livros]
    return jsonify(livros_json)

####### material didatico ########################################################################################################


@app.route('/add_material')
def add_material():
    material = MaterialDidatico(
        # ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
        Descricao="desc",
        Categoria="vateg",
        NumeroSerie="123",
        EstadoConservacao="afaf",
        LocalizacaoFisica="sehfjk",
        FotoMaterialURI="dhjsgf",
    )
    db.session.add(material)
    db.session.commit()
    return 'material add'


@app.route('/update_material/<id>', methods=['PUT'])
def update_material(id):
    material = MaterialDidatico.query.get(id)
    if material is None:
        return jsonify({'error': 'material não encontrado'}), 404

    data = request.json
    material.Descricao = data.get('Descricao', material.Descricao)
    material.Categoria = data.get('Categoria', material.Categoria)
    material.NumeroSerie = data.get('NumeroSerie', material.NumeroSerie)
    # material.DataAquisicao = data.get('DataAquisicao', material.DataAquisicao)
    material.EstadoConservacao = data.get(
        'EstadoConservacao', material.EstadoConservacao)
    material.LocalizacaoFisica = data.get(
        'LocalizacaoFisica', material.LocalizacaoFisica)
    material.FotoMaterialURI = data.get(
        'FotoMaterialUri', material.FotoMaterialURI)

    db.session.commit()
    return jsonify({'message': 'Material atualizado com sucesso'}), 200


@app.route('/delete_material/<id>', methods=['DELETE'])
def delete_material(id):
    livro = MaterialDidatico.query.get(id)
    if livro is None:
        return jsonify({'error': 'Material não encontrado'}), 404

    db.session.delete(livro)
    db.session.commit()
    return jsonify({'message': 'Material excluído com sucesso'}), 200


@app.route('/get_material/<id>')
def get_material(id):
    material = MaterialDidatico.query.get(id)
    if material is None:
        return jsonify({'error': 'Material não encontrado'}), 404

    material_json = {
        'ID': material.ID,
        'Descricao': material.Descricao,
        'Categoria': material.Categoria,
        'NumeroSerie': material.NumeroSerie,
        'DataAquisicao': material.DataAquisicao,
        'EstadoConservacao': material.EstadoConservacao,
        'LocalizacaoFisica': material.LocalizacaoFisica,
        'FotoMaterialURI': material.FotoMaterialURI
    }

    return jsonify(material_json)

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
