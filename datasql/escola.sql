// Criar o nó principal para o Instituto Piaget
CREATE (instituto:Instituto {nome: 'Instituto Piaget'});

// Criar nós para as diferentes sub-instituições do Instituto Piaget
CREATE (ip_almada:Instituto {nome: 'Instituto Piaget de Almada'}),
       (ip_silves:Instituto {nome: 'Instituto Piaget de Silves'}),
       (ip_gaia:Instituto {nome: 'Instituto Piaget de Vila Nova de Gaia'}),
       (ip_viseu:Instituto {nome: 'Instituto Piaget de Viseu'});

// Criar nós para as Escolas que fazem parte do Instituto Piaget
CREATE (ess_viseu:Escola {nome: 'Escola Superior de Saúde Jean Piaget Viseu'}),
       (esde_gaia:Escola {nome: 'Escola Superior de Desporto e Educação Jean Piaget Vila Nova de Gaia'}),
       (ess_gaia:Escola {nome: 'Escola Superior de Saúde Jean Piaget Vila Nova de Gaia'}),
       (ese_almada:Escola {nome: 'Escola Superior de Educação Jean Piaget Almada'}),
       (ess_almada:Escola {nome: 'Escola Superior de Saúde Jean Piaget Almada'}),
       (ess_algarve:Escola {nome: 'Escola Superior de Saúde Jean Piaget Algarve'}),
       (estg_almada:Escola {nome: 'Escola Superior de Tecnologia e Gestão Jean Piaget Almada'}),
       (iseit_almada:Escola {nome: 'ISEIT — Ensino Universitário em Almada'}),
       (iseit_viseu:Escola {nome: 'ISEIT — Ensino Universitário em Viseu'});

// Criar nós para os Institutos Politécnicos
CREATE (ip_norte:Instituto {nome: 'Instituto Politécnico Jean Piaget do Norte'}),
       (ip_sul:Instituto {nome: 'Instituto Politécnico Jean Piaget do Sul'});

// Associar as escolas ao Instituto Politécnico Jean Piaget do Norte
CREATE (esde_gaia:Escola {nome: 'Escola Superior de Desporto e Educação Jean Piaget Vila Nova de Gaia'}),
       (ess_gaia:Escola {nome: 'Escola Superior de Saúde Jean Piaget Vila Nova de Gaia'});

// Associar as escolas ao Instituto Politécnico Jean Piaget do Sul
CREATE (ese_almada:Escola {nome: 'Escola Superior de Educação Jean Piaget Almada'}),
       (ess_almada:Escola {nome: 'Escola Superior de Saúde Jean Piaget Almada'}),
       (ess_algarve:Escola {nome: 'Escola Superior de Saúde Jean Piaget Algarve'}),
       (estg_almada:Escola {nome: 'Escola Superior de Tecnologias e Gestão Almada'});


