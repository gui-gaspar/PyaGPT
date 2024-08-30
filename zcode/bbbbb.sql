//Apagar Relacoes 
MATCH ()-[r]->()
DELETE r;


// 1. Relacionar `Escola` com `Curso`
MATCH (e:Escola), (c:Curso)
WHERE e.nome = c.escola
MERGE (e)-[:OFERECE_CURSO]->(c);

// 2. Relacionar `Curso` com `CursoInfo`
MATCH (c:Curso), (ci:CursoInfo)
WHERE c.curso = ci.curso
MERGE (c)-[:TEM_INFO]->(ci);

// 3. Relacionar `Curso` com `Horários`
MATCH (c:Curso), (h:Horarios)
WHERE c.curso = h.curso
MERGE (c)-[:TEM_HORARIO]->(h);

// 4. Relacionar `Escola` com `Órgãos de Gestão`
MATCH (e:Escola), (o:OrgaosGestao)
WHERE e.nome = o.escola
MERGE (e)-[:GERIDO_POR]->(o);

// 5. Relacionar `Curso` com `PlanoEstudos`
MATCH (c:Curso), (p:PlanoEstudos)
WHERE c.curso = p.curso
MERGE (c)-[:TEM_PLANO_DE_ESTUDOS]->(p);

// 6. Relacionar `Instituto` com `Escola`
MATCH (i:Instituto), (e:Escola)
WHERE i.nome = e.nome
MERGE (i)-[:OFERECE]->(e);

// 7. Relacionar `Instituto` com `Contato`
MATCH (i:Instituto), (c:Contato)
WHERE i.nome = c.instituto
MERGE (i)-[:TEM_CONTATO]->(c);

// 8. Relacionar `Escola` com `Contato`
MATCH (e:Escola), (c:Contato)
WHERE e.nome = c.instituto
MERGE (e)-[:TEM_CONTATO]->(c);

// 9. Relacionar `Utilizadores` com `Curso`
MATCH (u:Utilizadores), (c:Curso)
WHERE u.curso = c.curso AND u.escola = c.escola
MERGE (u)-[:INSCRITO_EM]->(c);

// 10. Relacionar `Utilizadores` com `Escola`
MATCH (u:Utilizadores), (e:Escola)
WHERE u.escola = e.nome
MERGE (u)-[:PERTENCE_A]->(e);

// 11. Relacionar `Utilizadores` com `Instituto`
MATCH (u:Utilizadores), (i:Instituto)
WHERE u.instituto = i.nome
MERGE (u)-[:PERTENCE_A_INSTITUTO]->(i);


CALL db.relationshipTypes();