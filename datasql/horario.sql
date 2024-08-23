LOAD CSV WITH HEADERS FROM 'file:///horario_ei_3a.csv' AS linha
MERGE (h:Horario {
    curso: linha["Curso"], 
    ano: toInteger(linha["Ano"]),
    mes: linha["Mês"],
    dia_da_semana: linha["Dia"],
    dia_do_mes: toInteger(linha["Dia do Mês"]),
    hora_inicio: linha["Hora Início"],
    hora_fim: linha["Hora Fim"],
    cadeira: linha["Cadeira"],
    ano_academico: linha["Ano Acadêmico"]
})
RETURN h LIMIT 5;
