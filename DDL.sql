CREATE DATABASE IF NOT EXISTS Biblioteca;
GRANT ALL PRIVILEGES ON Biblioteca.* TO 'root'@'localhost';
USE Biblioteca;

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




DROP TRIGGER IF EXISTS datas_validas;
DROP TRIGGER IF EXISTS emprestimo_singularidade;

ALTER TABLE Usuarios
DROP CONSTRAINT IF EXISTS nomes_unicos;

ALTER TABLE Usuarios
ADD CONSTRAINT nomes_unicos UNIQUE (Nome);

DELIMITER //
CREATE TRIGGER datas_validas
BEFORE INSERT ON Emprestimos
FOR EACH ROW
BEGIN   
    IF NEW.DataEmprestimo < CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Aviso: Data de início de empréstimo no passado';
    END IF;
    IF NEW.DataDevolucaoPrevista <= CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Aviso: Data de devolução prevista no passado ou hoje';
    END IF;
    IF NEW.DataDevolucaoPrevista <= NEW.DataEmprestimo THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Aviso: Data de devolução prevista anterior à data de início';
    END IF;
END;
//
DELIMITER ;



DELIMITER //

CREATE TRIGGER emprestimo_singularidade
BEFORE INSERT ON Emprestimos
FOR EACH ROW
BEGIN
    DECLARE emprestimo_exists INT;

    -- Verifica se o empréstimo já existe e possui data de devolução prevista no passado
    SELECT COUNT(*) INTO emprestimo_exists
    FROM Emprestimos
    WHERE IDUsuario = NEW.IDUsuario AND IDLivro = NEW.IDLivro AND DataDevolucaoPrevista < CURDATE();

    IF emprestimo_exists > 0 THEN
        DELETE FROM Emprestimos
        WHERE IDUsuario = NEW.IDUsuario AND IDLivro = NEW.IDLivro;
    END IF;
END;
//
DELIMITER ;

