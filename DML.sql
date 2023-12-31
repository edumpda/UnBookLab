-- Insert data into the Livros table
INSERT INTO Livros (ISBN, Titulo, Autor, Descricao, Categoria, DataAquisicao, EstadoConservacao, LocalizacaoFisica, CapaLivroURI)
VALUES ('9783161484100', 'Desenvolvimento de Software', 'Alberto Souza', 'Aprenda a criar aplicativos para dispositivos móveis', 'Programação', '2022-01-01', 'Bom', 'Sala de Reuniões', 'livro1.jpg');

INSERT INTO Livros (ISBN, Titulo, Autor, Descricao, Categoria, DataAquisicao, EstadoConservacao, LocalizacaoFisica, CapaLivroURI)
VALUES ('9783161484117', 'Gestão de Projetos', 'Carlos Azevedo', 'Aprenda a liderar e gerenciar projetos de software', 'Gestão', '2022-01-01', 'Bom', 'Sala de Reuniões', 'livro2.jpg');

INSERT INTO Livros (ISBN, Titulo, Autor, Descricao, Categoria, DataAquisicao, EstadoConservacao, LocalizacaoFisica, CapaLivroURI)
VALUES ('9783161484124', 'Inteligência Artificial', 'Ana Souza', 'Aprenda a criar e treinar modelos de inteligência artificial', 'Inteligência Artificial', '2022-01-01', 'Bom', 'Sala de Reuniões', 'livro3.jpg');

-- Insert data into the MateriaisDidaticos table
INSERT INTO MateriaisDidaticos (ID, Descricao, Categoria, NumeroSerie, DataAquisicao, EstadoConservacao, LocalizacaoFisica, FotoMaterialURI)
VALUES (1, 'Cálculo I', 'Matemática', 'MS001', '2022-01-01', 'Bom', 'Sala de Aula', 'material1.jpg');

INSERT INTO MateriaisDidaticos (ID, Descricao, Categoria, NumeroSerie, DataAquisicao, EstadoConservacao, LocalizacaoFisica, FotoMaterialURI)
VALUES (2, 'Estatística I', 'Matemática', 'MS002', '2022-01-01', 'Bom', 'Sala de Aula', 'material2.jpg');

INSERT INTO MateriaisDidaticos (ID, Descricao, Categoria, NumeroSerie, DataAquisicao, EstadoConservacao, LocalizacaoFisica, FotoMaterialURI)
VALUES (3, 'Sistemas Operacionais I', 'Sistemas', 'MS003', '2022-01-01', 'Bom', 'Sala de Aula', 'material3.jpg');

-- Insert data into the Usuarios table
INSERT INTO Usuarios (ID, Nome, Sobrenome, Funcao, Login, SenhaCriptografada, FotoUsuarioURI)
VALUES (1, 'Carlos', 'Silva', 'Desenvolvedor', 'carlos.silva', 'sha256$RoZrEycUXtIpMVEl$624f17d0219f83c66d96233e4e03a9a68dca3ac906622b16c3fa3246b9c47578', 'usuario1.jpg');

INSERT INTO Usuarios (ID, Nome, Sobrenome, Funcao, Login, SenhaCriptografada, FotoUsuarioURI)
VALUES (2, 'Maria', 'Souza', 'Gerente de Projetos', 'maria.souza', 'sha256$bluaIK5MpjWZnSam$a46e315eb219889a92b84ccaeba1f487d87422434b4cad7b1d9a2f492405812a', 'usuario2.jpg');

INSERT INTO Usuarios (ID, Nome, Sobrenome, Funcao, Login, SenhaCriptografada, FotoUsuarioURI)
VALUES (3, 'João', 'Ferreira', 'Técnico em Informática', 'joao.ferreira', 'sha256$tqL3XduUvhTh6EYJ$60cb0665d4db89961776ac37b3d9dacaed6573289082aa0ba11e0971aed8abc5', 'usuario3.jpg');

INSERT INTO Emprestimos (IDUsuario, IDLivro, IDMaterialDidatico, DataEmprestimo, DataDevolucaoPrevista, Status)
VALUES (1, '9783161484100', 2, '2024-11-14', '2024-11-28', 'Em andamento');
INSERT INTO Emprestimos (IDUsuario, IDLivro, IDMaterialDidatico, DataEmprestimo, DataDevolucaoPrevista, Status)
VALUES (1, '9783161484117', 2, '2024-11-14', '2024-11-28', 'Em andamento');
INSERT INTO Emprestimos (IDUsuario, IDLivro, IDMaterialDidatico, DataEmprestimo, DataDevolucaoPrevista, Status)
VALUES (1, '9783161484124', 2, '2024-11-14', '2024-11-28', 'Em andamento');