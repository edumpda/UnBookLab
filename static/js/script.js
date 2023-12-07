function pesquisarLivro() {
    const isbnPesquisa = document.getElementById('isbn_pesquisa').value;

    fetch(`/get_livro?isbn=${isbnPesquisa}`)
        .then(response => response.json())
        .then(data => {
            const livroInfoDiv = document.getElementById('livro_info');
            if (data.error) {
                livroInfoDiv.innerHTML = `<p>${data.error}</p>`;
            } else {
                const livroInfoHTML = `
                    <p><strong>ISBN:</strong> ${data.ISBN}</p>
                    <p><strong>Título:</strong> ${data.Titulo}</p>
                    <p><strong>Autor:</strong> ${data.Autor}</p>
                    <!-- Adicione outros campos conforme necessário -->
                `;
                livroInfoDiv.innerHTML = livroInfoHTML;
            }
        })
        .catch(error => {
            console.error('Erro:', error);
        });
}

function listarLivros() {
    fetch('/get_livros')
        .then(response => response.json())
        .then(data => {
            const livrosListagemUl = document.getElementById('livros_listagem');
            livrosListagemUl.innerHTML = '';

            if (data.length === 0) {
                livrosListagemUl.innerHTML = '<p>Nenhum livro encontrado.</p>';
            } else {
                data.forEach(livro => {
                    const livroItem = document.createElement('li');
                    livroItem.textContent = `ISBN: ${livro.ISBN} | Título: ${livro.Titulo} | Autor: ${livro.Autor}`;
                    livrosListagemUl.appendChild(livroItem);
                });
            }
        })
        .catch(error => {
            console.error('Erro:', error);
        });
}
