CREATE (u:Utilizador {
    username: 'admin',
    password: 'admin_password',
    nome_completo: 'Ana Pereira',
    email: 'ana.pereira@exemplo.com',
    telefone: '912-345-678',
    endereco: 'Avenida Central, 100, Lisboa',
    tipo_utilizador: 'admin',
    informacao_adicional: 'Administrador do sistema'
});



CREATE (u:Utilizador {
    username: 'estudante1',
    password: 'estudante_password',
    nome_completo: 'João da Silva',
    email: 'joao.silva@exemplo.com',
    telefone: '987-654-321',
    endereco: 'Rua da Felicidade, 45, Almada',
    curso: 'Engenharia Informática',
    tipo_curso: 'Licenciatura',
    escola: 'Escola Superior de Tecnologias e Gestão Jean Piaget Almada',
    tipo_utilizador: 'estudante',
    informacao_adicional: 'Estudante do 2.º ano'
});
