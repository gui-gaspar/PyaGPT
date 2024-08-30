LOAD CSV WITH HEADERS FROM 'file:///horario_ei_3a.csv' AS linha
WITH
    CASE WHEN linha["Ano"] IS NOT NULL AND linha["Ano"] <> "" AND NOT linha["Ano"] = "NaN" THEN toInteger(linha["Ano"]) ELSE null END AS ano,
    CASE WHEN linha["Curso"] IS NOT NULL AND linha["Curso"] <> "" THEN linha["Curso"] ELSE null END AS curso,
    CASE WHEN linha["Mês"] IS NOT NULL AND linha["Mês"] <> "" THEN linha["Mês"] ELSE null END AS mes,
    CASE WHEN linha["Dia"] IS NOT NULL AND linha["Dia"] <> "" THEN linha["Dia"] ELSE null END AS dia_da_semana,
    CASE WHEN linha["Dia do Mês"] IS NOT NULL AND linha["Dia do Mês"] <> "" AND NOT linha["Dia do Mês"] = "NaN" THEN toInteger(linha["Dia do Mês"]) ELSE null END AS dia_do_mes,
    CASE WHEN linha["Hora Início"] IS NOT NULL AND linha["Hora Início"] <> "" THEN linha["Hora Início"] ELSE null END AS hora_inicio,
    CASE WHEN linha["Hora Fim"] IS NOT NULL AND linha["Hora Fim"] <> "" THEN linha["Hora Fim"] ELSE null END AS hora_fim,
    CASE WHEN linha["Cadeira"] IS NOT NULL AND linha["Cadeira"] <> "" THEN linha["Cadeira"] ELSE null END AS cadeira,
    CASE WHEN linha["Ano Acadêmico"] IS NOT NULL AND linha["Ano Acadêmico"] <> "" THEN linha["Ano Acadêmico"] ELSE null END AS ano_academico
WHERE ano IS NOT NULL AND dia_do_mes IS NOT NULL
MERGE (h:Horarios {
    curso: curso,
    ano: ano,
    mes: mes,
    dia_da_semana: dia_da_semana,
    dia_do_mes: dia_do_mes,
    hora_inicio: hora_inicio,
    hora_fim: hora_fim,
    cadeira: cadeira,
    ano_academico: ano_academico
})
RETURN h
LIMIT 5;
