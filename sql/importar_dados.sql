//Apagar todos os Dados
MATCH (n) DETACH DELETE n;



// Contatos
LOAD CSV WITH HEADERS FROM 'file:///contatos.csv' AS row
CREATE (c:Contato {
    instituto: row.Instituto,
    tipo: row.Tipo,
    morada: row.Morada,
    codigo_postal: row.Codigo_Postal,
    telefone: row.Telefone,
    fax: row.Fax,
    email: row.Email,
    gps: row.GPS,
    skype: row.Skype,
    horario: row.Horario
});

// Cursos
LOAD CSV WITH HEADERS FROM 'file:///cursos.csv' AS row
CREATE (c:Curso {
    tipo: row.Tipo,
    curso: row.Curso,
    escola: row.Escola
});

// Curso Info
LOAD CSV WITH HEADERS FROM 'file:///curso_info.csv' AS row
CREATE (c:CursoInfo {
    curso: row.Curso,
    saídas_profissionais: row['Saídas Profissionais'],
    estatuto_profissional: row['Estatuto Profissional'],
    apresentação: row['Apresentação'],
    acesso_a_outros_ciclos: row['Acesso a Outros Ciclos'],
    área_de_estudo: row['Área de Estudo'],
    regras_de_avaliação: row['Regras de Avaliação'],
    acesso: row['Acesso'],
    diploma: row['Diploma']
});

// Plano Estudos
LOAD CSV WITH HEADERS FROM 'file:///plano_estudos.csv' AS row
CREATE (p:PlanoEstudos {
    tipo: row.Tipo,
    curso: row.Curso,
    ano: row.Ano,
    semestre: row.Semestre,
    unidade_curricular: row.UnidadeCurricular,
    ch: row['CH'],
    ects: row.ECTS
});

// Horarios
LOAD CSV WITH HEADERS FROM 'file:///horario_ei_3a.csv' AS row
CREATE (h:Horarios {
    curso: row.Curso,
    ano: row.Ano,
    mes: row.Mês,
    dia: row.Dia,
    dia_do_mes: row['Dia do Mês'],
    hora_inicio: row['Hora Início'],
    hora_fim: row['Hora Fim'],
    cadeira: row.Cadeira,
    ano_academico: row['Ano Acadêmico']
});

// Institutos / Escolas
LOAD CSV WITH HEADERS FROM 'file:///institutos_escolas.csv' AS row
WITH row, 
     CASE 
         WHEN row.Instituto IS NOT NULL AND row.Instituto <> '' THEN row.Instituto
         ELSE 'Não Definido' 
     END AS instituto_nome
MERGE (e:Escola { nome: row.Nome, descricao: row['Descricao'] })
WITH e, instituto_nome
MERGE (i:Instituto { nome: instituto_nome });


// Orgaos Gestao
LOAD CSV WITH HEADERS FROM 'file:///orgaos_de_gestao.csv' AS row
CREATE (o:OrgaosGestao {
    escola: row.Escola,
    função: row['Função'],
    nome: row.Nome
});

// Utilizadores
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
    instituto: 'Instituto Piaget de Almada', 
    tipo_utilizador: 'estudante',
    informacao_adicional: 'N/A'
});

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
