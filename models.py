from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
db = SQLAlchemy()

class Livros(db.Model):
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
<<<<<<< Updated upstream
    __tablename__ = 'materiaisdidaticos'  # Defina o nome correto da tabela no banco de dados

    ID = db.Column(db.Integer, primary_key=True)
    Descricao = db.Column(db.String(255))
    Categoria = db.Column(db.String(255))
    NumeroSerie = db.Column(db.String(50))
    DataAquisicao = db.Column(db.Date, default=db.func.current_date())
=======
    __tablename__ = 'materiaisdidaticos'  # Adicione esta linha
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Descricao = db.Column(db.Text)
    Categoria = db.Column(db.String(50))
    NumeroSerie = db.Column(db.String(20))
    DataAquisicao = db.Column(db.Date)
>>>>>>> Stashed changes
    EstadoConservacao = db.Column(db.String(50))
    LocalizacaoFisica = db.Column(db.String(255))
    FotoMaterialURI = db.Column(db.String(255))


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(255))
    Sobrenome = db.Column(db.String(255))
    Funcao = db.Column(db.String(50))
    Login = db.Column(db.String(50))
    SenhaCriptografada = db.Column(db.String(255))
    FotoUsuarioURI = db.Column(db.String(255))
    
class Emprestimo(db.Model):
<<<<<<< Updated upstream
    __tablename__ = 'emprestimos'

    ID = db.Column(db.Integer, primary_key=True)
    IDUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.ID'))  # Adicione a chave estrangeira para usuarios
    IDLivro = db.Column(db.String(20), db.ForeignKey('livros.ISBN'))
    IDMaterialDidatico = db.Column(db.Integer, db.ForeignKey('materiaisdidaticos.ID'))
    DataEmprestimo = db.Column(db.Date, default=db.func.current_date())
    DataDevolucaoPrevista = db.Column(db.Date)
    Status = db.Column(db.String(50))

    usuario = db.relationship('Usuario', backref=db.backref('emprestimos', lazy='dynamic'))
=======
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IDUsuario = db.Column(db.Integer, db.ForeignKey('usuario.ID'))
    IDLivro = db.Column(db.String(13), db.ForeignKey('livros.ISBN'))
    IDMaterialDidatico = db.Column(db.Integer, db.ForeignKey('materialdidatico.ID'))
    DataEmprestimo = db.Column(db.Date)
    DataDevolucaoPrevista = db.Column(db.Date)
    Status = db.Column(db.String(50))

    usuario = relationship('Usuario', foreign_keys=[IDUsuario])
    livro = relationship('Livros', foreign_keys=[IDLivro])
    material_didatico = relationship('MaterialDidatico', foreign_keys=[IDMaterialDidatico], primaryjoin='Emprestimo.IDMaterialDidatico == MaterialDidatico.ID')

    def __init__(self, IDUsuario, IDLivro, IDMaterialDidatico, DataEmprestimo, DataDevolucaoPrevista, Status):
        self.IDUsuario = IDUsuario
        self.IDLivro = IDLivro
        self.IDMaterialDidatico = IDMaterialDidatico
        self.DataEmprestimo = DataEmprestimo
        self.DataDevolucaoPrevista = DataDevolucaoPrevista
        self.Status = Status
>>>>>>> Stashed changes
