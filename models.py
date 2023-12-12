from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Livros(db.Model):
    Livros = 'livros'
    ISBN = db.Column(db.String(13), primary_key=True)
    Titulo = db.Column(db.String(255))
    Autor = db.Column(db.String(255))
    Descricao = db.Column(db.Text)
    Categoria = db.Column(db.String(50))
    DataAquisicao = db.Column(db.Date)
    EstadoConservacao = db.Column(db.String(50))
    LocalizacaoFisica = db.Column(db.String(255))
    CapaLivroURI = db.Column(db.String(255))


class MaterialDidatico(db.Model):
    MaterialDidatico = 'material_didatico'  # Nome da tabeela no seu BD
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Descricao = db.Column(db.Text)
    Categoria = db.Column(db.String(50))
    NumeroSerie = db.Column(db.String(20))
    DataAquisicao = db.Column(db.Date)
    EstadoConservacao = db.Column(db.String(50))
    LocalizacaoFisica = db.Column(db.String(255))
    FotoMaterialURI = db.Column(db.String(255))


class Usuario(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(255))
    Sobrenome = db.Column(db.String(255))
    Funcao = db.Column(db.String(50))
    Login = db.Column(db.String(50))
    SenhaCriptografada = db.Column(db.String(255))
    FotoUsuarioURI = db.Column(db.String(255))


class Emprestimo(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IDUsuario = db.Column(db.Integer, db.ForeignKey('usuario.ID'))
    IDLivro = db.Column(db.String(13), db.ForeignKey('livros.ISBN'))
    IDMaterialDidatico = db.Column(
        db.Integer, db.ForeignKey('material_didatico.ID'))
    DataEmprestimo = db.Column(db.Date)
    DataDevolucaoPrevista = db.Column(db.Date)
    Status = db.Column(db.String(50))

    usuario = db.relationship('Usuario', foreign_keys=[IDUsuario])
    livro = db.relationship('Livros', foreign_keys=[IDLivro])
    material_didatico = db.relationship('MaterialDidatico', foreign_keys=[
                                        IDMaterialDidatico], primaryjoin='Emprestimo.IDMaterialDidatico == MaterialDidatico.ID')
