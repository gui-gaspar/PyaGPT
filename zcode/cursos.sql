LOAD CSV WITH HEADERS FROM 'file:///cursos.csv' AS row
CREATE (c:Cursos {tipo: row.tipo, nome: row.curso});

