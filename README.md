# UnBookLab

Este projeto é uma aplicação web para gerenciar uma biblioteca virtual, permitindo o gerenciamento de livros, materiais didáticos e empréstimos.

## Configuração e Execução

Siga os passos abaixo para configurar e executar o projeto:

```bash
# Clonar este repositório
git clone https://github.com/edumpda/UnBookLab.git

# Mudar o diretório corrente para o do repositório
cd UnBookLab

# Instalar dependências
pip install -r requirements.txt

# Fazer login no MySQL (linha de comando, workbench etc)
mysql -u root -p

# Criar usuário MySQL
CREATE USER 'unbooklab_admin'@'localhost' IDENTIFIED BY 'senha';

# Criar database
CREATE DATABASE Biblioteca;

# Organizar estrutura do banco de dados \\ outra alternativa é executar o ddl.sql na interface mysql
mysql -u root -p Biblioteca < ./DDL.sql

# Popular banco de dados com 3 linhas para cada tabela
mysql -u root -p Biblioteca < ./DML.sql

# Sair do ambiente MySQL, caso esteja dentro
exit;

# Executar a aplicação
python app.py
