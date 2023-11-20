from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Livros, MaterialDidatico, Usuario, Emprestimo
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chave'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    livro = Livros(ISBN='9788575221631', Titulo='Guia Mangá de Bancos de Dados', Autor='Mana Takahashi', Descricao='Descrição grande demais', Categoria='Educação', DataAquisicao=datetime.strptime('2023-11-19', '%Y-%m-%d').date(), EstadoConservacao='Novo', LocalizacaoFisica='Estante 1', CapaLivroURI='https://s3-sa-east-1.amazonaws.com/catalogodasartes/obra_13269947.jpg')
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
    livro.DataAquisicao = datetime.strptime(data.get('DataAquisicao', livro.DataAquisicao), '%Y-%m-%d').date()
    livro.EstadoConservacao = data.get('EstadoConservacao', livro.EstadoConservacao)
    livro.LocalizacaoFisica = data.get('LocalizacaoFisica', livro.LocalizacaoFisica)
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


if __name__ == '__main__':
    app.run(debug=True)
