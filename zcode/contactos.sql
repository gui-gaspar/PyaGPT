LOAD CSV WITH HEADERS FROM 'file:///contatos.csv' AS row
MERGE (c:Contatos {instituto: row.instituto, tipo: row.tipo})
SET c.morada = row.morada,
    c.codigo_postal = row.codigo_postal,
    c.telefone = row.telefone,
    c.fax = row.fax,
    c.email = row.email,
    c.gps = row.gps,
    c.nome = row.nome,
    c.skype = row.skype,
    c.horario = row.horario;
