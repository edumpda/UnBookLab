def initialize(data):
    emp_json = {
        "id": data[0],
        'id_usuario': data[1],
        'id_livro': data[2],
        'id_material': data[3],
        'data_emprestimo': data[4],
        'data_devolucao': data[5]
    }
    return emp_json
