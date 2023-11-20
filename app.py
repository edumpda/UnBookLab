from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Livros, MaterialDidatico, Usuario, Emprestimo

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
    livro = Livros(ISBN='9788575221631', Titulo='Guia Mangá de Bancos de Dados', Autor='Mana Takahashi', Descricao='Descrição grande demais', Categoria='Educação', DataAquisicao='2023-11-19', EstadoConservacao='Novo', LocalizacaoFisica='Estante 1', CapaLivroURI='https://s3-sa-east-1.amazonaws.com/catalogodasartes/obra_13269947.jpg')
    db.session.add(livro)
    db.session.commit()
    return 'Livro adicionado'

@app.route('/get_livros')
def get_livros():
    livros = Livros.query.all()
    livros_json = [{'ISBN': livro.ISBN, 'Titulo': livro.Titulo, 'Autor': livro.Autor} for livro in livros]
    return jsonify(livros_json)

if __name__ == '__main__':
    app.run(debug=True)
