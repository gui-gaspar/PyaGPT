CREATE (u:Utilizadores {
    username: 'admin',
    password: 'admin',
    nome_completo: 'Admin',
    email: 'admin@ipiaget.pt',
    telefone: '912345678',
    morada: 'Avenida Central, 100, Lisboa',
    tipo_utilizador: 'admin',
    informacao_adicional: 'Administrador do sistema'
});

CREATE (u:Utilizadores {
    username: 'guigaspar',
    password: 'guigaspar',
    nome_completo: 'Guilherme Gaspar',
    email: '60434@ipiaget.pt',
    telefone: '913468499',
    morada: 'Rua da Felicidade, 45, Almada',
    curso: 'Engenharia Informática',
    tipo_curso: 'Licenciatura',
    escola: 'Escola Superior de Tecnologia e Gestão Jean Piaget Almada',
    tipo_utilizador: 'estudante',
    informacao_adicional: 'N/A'
});
