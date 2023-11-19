CREATE DATABASE IF NOT EXISTS Biblioteca;
USE Biblioteca;
GRANT ALL PRIVILEGES ON Biblioteca TO 'unbooklab_admin'@'localhost';
GRANT ALL PRIVILEGES ON Biblioteca.* TO 'unbooklab_admin'@'localhost';

CREATE TABLE IF NOT EXISTS Livros (
    ISBN varchar(13) PRIMARY KEY,
    Titulo varchar(255),
    Autor varchar(255),
    Descricao text,
    Categoria varchar(50),
    DataAquisicao date,
    EstadoConservacao varchar(50),
    LocalizacaoFisica varchar(255),
    CapaLivroURI varchar(255)
);

CREATE TABLE IF NOT EXISTS MateriaisDidaticos (
    ID int PRIMARY KEY AUTO_INCREMENT,
    Descricao text,
    Categoria varchar(50),
    NumeroSerie varchar(20),
    DataAquisicao date,
    EstadoConservacao varchar(50),
    LocalizacaoFisica varchar(255),
    FotoMaterialURI varchar(255)
);

CREATE TABLE IF NOT EXISTS Usuarios (
    ID int PRIMARY KEY AUTO_INCREMENT,
    Nome varchar(255),
    Sobrenome varchar(255),
    Funcao varchar(50),
    Login varchar(50),
    SenhaCriptografada varchar(255),
    FotoUsuarioURI varchar(255)
);

CREATE TABLE IF NOT EXISTS Emprestimos (
    ID int PRIMARY KEY AUTO_INCREMENT,
    IDUsuario int,
    IDLivro varchar(13),
    IDMaterialDidatico int,
    DataEmprestimo date,
    DataDevolucaoPrevista date,
    Status varchar(50),
    FOREIGN KEY (IDUsuario) REFERENCES Usuarios(ID),
    FOREIGN KEY (IDLivro) REFERENCES Livros(ISBN),
    FOREIGN KEY (IDMaterialDidatico) REFERENCES MateriaisDidaticos(ID)
);