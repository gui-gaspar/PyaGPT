// Criar nós para Licenciaturas
CREATE 
    (lic_Desporto:Curso {nome: 'Desporto', tipo: 'Licenciatura'}),
    (lic_EducacaoBasica:Curso {nome: 'Educação Básica', tipo: 'Licenciatura'}),
    (lic_EducacaoFisicaDesporto:Curso {nome: 'Educação Física e Desporto', tipo: 'Licenciatura'}),
    (lic_EducacaoSocial:Curso {nome: 'Educação Social', tipo: 'Licenciatura'}),
    (lic_Enfermagem:Curso {nome: 'Enfermagem', tipo: 'Licenciatura'}),
    (lic_EngenhariaInformatica:Curso {nome: 'Engenharia Informática', tipo: 'Licenciatura'}),
    (lic_Fisioterapia:Curso {nome: 'Fisioterapia', tipo: 'Licenciatura'}),
    (lic_Gestao:Curso {nome: 'Gestão', tipo: 'Licenciatura'}),
    (lic_MedicinaChinesa:Curso {nome: 'Medicina Tradicional Chinesa', tipo: 'Licenciatura'}),
    (lic_Osteopatia:Curso {nome: 'Osteopatia', tipo: 'Licenciatura'}),
    (lic_Psicologia:Curso {nome: 'Psicologia', tipo: 'Licenciatura'}),
    (lic_RelacoesInternacionais:Curso {nome: 'Relações Internacionais', tipo: 'Licenciatura'});

// Criar nós para Mestrados
CREATE 
    (mes_EducacaoPreEscolar:Curso {nome: 'Educação Pré-Escolar e Ensino do 1.º Ciclo do Ensino Básico', tipo: 'Mestrado'}),
    (mes_EnfermagemMental:Curso {nome: 'Enfermagem de Saúde Mental e Psiquiátrica', tipo: 'Mestrado'}),
    (mes_EnfermagemCritica:Curso {nome: 'Enfermagem Médico-Cirúrgica na área de Enfermagem à Pessoa em Situação Crítica', tipo: 'Mestrado'}),
    (mes_EducacaoFisica:Curso {nome: 'Ensino de Educação Física nos Ensinos Básico e Secundário', tipo: 'Mestrado'}),
    (mes_ExercicioSaude:Curso {nome: 'Exercício e Saúde', tipo: 'Mestrado'}),
    (mes_PsicologiaEducacao:Curso {nome: 'Psicologia da Educação e Aconselhamento', tipo: 'Mestrado'}),
    (mes_PsicologiaSocial:Curso {nome: 'Psicologia Social e das Organizações', tipo: 'Mestrado'});

// Criar nós para CTeSP (Cursos Técnicos Superiores Profissionais)
CREATE 
    (ctesp_AnaliseDados:Curso {nome: 'Análise de Dados em Gestão de Informação', tipo: 'CTeSP'}),
    (ctesp_AnimacaoDigital:Curso {nome: 'Animação, Modelação e Desenho Digital', tipo: 'CTeSP'}),
    (ctesp_AssessoriaGestao:Curso {nome: 'Assessoria e Gestão Administrativa', tipo: 'CTeSP'}),
    (ctesp_Ciberseguranca:Curso {nome: 'Cibersegurança', tipo: 'CTeSP'}),
    (ctesp_DesenvolvimentoVideojogos:Curso {nome: 'Desenvolvimento de Videojogos e Aplicações Multimédia', tipo: 'CTeSP'}),
    (ctesp_DesportoLazer:Curso {nome: 'Desporto, Lazer e Bem-Estar', tipo: 'CTeSP'}),
    (ctesp_DesportosNatureza:Curso {nome: 'Desportos de Natureza e Animação Desportiva', tipo: 'CTeSP'}),
    (ctesp_EletronicaAutomacao:Curso {nome: 'Eletrónica e Automação', tipo: 'CTeSP'}),
    (ctesp_ExercicioSaude:Curso {nome: 'Exercício Físico e Saúde', tipo: 'CTeSP'}),
    (ctesp_Gerontologia:Curso {nome: 'Gerontologia', tipo: 'CTeSP'}),
    (ctesp_GestaoClinica:Curso {nome: 'Gestão Clínica Administrativa', tipo: 'CTeSP'}),
    (ctesp_InfraestruturasCloud:Curso {nome: 'Infraestruturas Cloud, Redes e Datacenter', tipo: 'CTeSP'}),
    (ctesp_IntervencaoEducativa:Curso {nome: 'Intervenção Educativa em Creche', tipo: 'CTeSP'}),
    (ctesp_IntervencaoSocioeducativa:Curso {nome: 'Intervenção Socioeducativa e Desenvolvimento Comunitário', tipo: 'CTeSP'}),
    (ctesp_MarketingVendas:Curso {nome: 'Marketing e Vendas', tipo: 'CTeSP'}),
    (ctesp_ProgramacaoWeb:Curso {nome: 'Programação em Web, Dispositivos e Aplicações Móveis', tipo: 'CTeSP'}),
    (ctesp_ServicoFamiliar:Curso {nome: 'Serviço Familiar e Comunitário', tipo: 'CTeSP'}),
    (ctesp_ServicoSocial:Curso {nome: 'Serviço Social e Desenvolvimento Comunitário', tipo: 'CTeSP'}),
    (ctesp_TermalismoBemEstar:Curso {nome: 'Termalismo e Bem-Estar', tipo: 'CTeSP'});

// Criar nós para Pós-Graduações
CREATE 
    (pg_EnfermagemAnestesia:Curso {nome: 'Enfermagem de Bloco Operatório: Enfermagem de Anestesia', tipo: 'Pós-Graduação'}),
    (pg_EnfermagemInstrumentacao:Curso {nome: 'Enfermagem de Bloco Operatório: Instrumentação Cirúrgica', tipo: 'Pós-Graduação'}),
    (pg_EnfermagemBlocoCompleto:Curso {nome: 'Enfermagem de Bloco Operatório: Instrumentação Cirúrgica e Enfermagem de Anestesia', tipo: 'Pós-Graduação'}),
    (pg_EnfermagemTrabalho:Curso {nome: 'Enfermagem do Trabalho', tipo: 'Pós-Graduação'}),
    (pg_EnfermagemReprocessamento:Curso {nome: 'Enfermagem em Reprocessamento de Dispositivos', tipo: 'Pós-Graduação'}),
    (pg_EnfermagemPrevencao:Curso {nome: 'Enfermagem em Reprocessamento de Dispositivos e em Prevenção e Controlo de Infeção e Resistência aos Antimicrobianos', tipo: 'Pós-Graduação'}),
    (pg_FisioterapiaDesporto:Curso {nome: 'Fisioterapia no Desporto', tipo: 'Pós-Graduação'}),
    (pg_GerontoGeriatria:Curso {nome: 'Geronto-geriatria', tipo: 'Pós-Graduação'}),
    (pg_PrevencaoInfeccao:Curso {nome: 'Prevenção e Controlo de Infeção e Resistência aos Antimicrobianos', tipo: 'Pós-Graduação'}),
    (pg_PsicologiaOcupacional:Curso {nome: 'Psicologia da Saúde Ocupacional', tipo: 'Pós-Graduação'}),
    (pg_SaudePublicaQualidade:Curso {nome: 'Saúde Pública e Gestão da Qualidade Alimentar', tipo: 'Pós-Graduação'}),
    (pg_SupervisaoClinica:Curso {nome: 'Supervisão Clínica na Formação e Desenvolvimento Profissional de Enfermeiros', tipo: 'Pós-Graduação'}),
    (pg_SupervisaoEnfermeiros:Curso {nome: 'Supervisão Clínica para Enfermeiros', tipo: 'Pós-Graduação'}),
    (pg_SupervisaoProfissionais:Curso {nome: 'Supervisão Clínica para Profissionais de Saúde', tipo: 'Pós-Graduação'}),
    (pg_TermalismoTurismoSPA:Curso {nome: 'Termalismo, Turismo e SPA', tipo: 'Pós-Graduação'}),

    (pg_GestaoUnidadesSaude:Curso {nome: 'Administração e Gestão de Unidades de Saúde', tipo: 'Pós-Graduação'}),
    (pg_GestaoSaudeRH:Curso {nome: 'Administração e Gestão de Unidades de Saúde e Gestão de Recursos Humanos', tipo: 'Pós-Graduação'}),
    (pg_AdministracaoEscolar:Curso {nome: 'Administração Escolar', tipo: 'Pós-Graduação'}),
    (pg_BibliotecasEscolares:Curso {nome: 'Bibliotecas Escolares — Gestão e Animação', tipo: 'Pós-Graduação'}),
    (pg_GestaoRH:Curso {nome: 'Gestão de Recursos Humanos', tipo: 'Pós-Graduação'}),
    (pg_GestaoEconomiaSocial:Curso {nome: 'Gestão de Serviços de Economia Social', tipo: 'Pós-Graduação'}),
    (pg_GestaoEscolar:Curso {nome: 'Gestão e Administração Escolar', tipo: 'Pós-Graduação'}),
    (pg_EstrategicaRH:Curso {nome: 'Gestão Estratégica de Recursos Humanos', tipo: 'Pós-Graduação'}),
    (pg_EstrategicaRH_Economia:Curso {nome: 'Gestão Estratégica de Recursos Humanos e Gestão de Serviços de Economia Social', tipo: 'Pós-Graduação'}),
    (pg_InovacaoQualidadeSaude:Curso {nome: 'Inovação, Gestão da Qualidade e Auditoria em Saúde', tipo: 'Pós-Graduação'}),
    (pg_LiderancaNegocios:Curso {nome: 'Liderança e Negócios', tipo: 'Pós-Graduação'}),
    (pg_RelacoesInternacionais:Curso {nome: 'Relações Internacionais — A Nova (des)Ordem Mundial: Abordagens Regionais para a Paz e os Conflitos', tipo: 'Pós-Graduação'}),
    (pg_SaudePublicaGestaoAlimentar:Curso {nome: 'Saúde Pública e Gestão da Qualidade Alimentar', tipo: 'Pós-Graduação'}),

    (pg_BibliotecasEscolaresEducacao:Curso {nome: 'Bibliotecas Escolares — Gestão e Animação', tipo: 'Pós-Graduação'}),
    (pg_DocenciaEnsinoSuperior:Curso {nome: 'Docência no Ensino Superior', tipo: 'Pós-Graduação'}),
    (pg_EducacaoCreche:Curso {nome: 'Educação em Creche — Intervenção e Animação Educativa', tipo: 'Pós-Graduação'}),
    (pg_EducacaoEspecialCognitivo:Curso {nome: 'Educação Especial: Domínio Cognitivo e Motor', tipo: 'Pós-Graduação'}),
    (pg_EducacaoEspecialAudicao:Curso {nome: 'Educação Especial: Domínio da Audição e Surdez', tipo: 'Pós-Graduação'}),
    (pg_EducacaoEspecialBaixaVisao:Curso {nome: 'Educação Especial: Domínio da Baixa Visão e Cegueira', tipo: 'Pós-Graduação'}),
    (pg_EducacaoEspecialPrecoce:Curso {nome: 'Educação Especial: Domínio da Intervenção Precoce na Infância', tipo: 'Pós-Graduação'}),
    (pg_IntervencaoComunitaria:Curso {nome: 'Intervenção Comunitária', tipo: 'Pós-Graduação'}),
    (pg_PortuguesLinguaNaoMaterna:Curso {nome: 'Português Língua Não Materna', tipo: 'Pós-Graduação'}),
    (pg_SupervisaoPedagogica:Curso {nome: 'Supervisão Pedagógica e Avaliação em Educação', tipo: 'Pós-Graduação'}),

    (pg_CibersegurancaAP:Curso {nome: 'Cibersegurança e Proteção de Dados na Administração Pública', tipo: 'Pós-Graduação'}),
    (pg_TecnologiasInformacao:Curso {nome: 'Tecnologias de Informação e Comunicação: Ecossistemas Híbridos de Aprendizagem', tipo: 'Pós-Graduação'}),
    (pg_TransformacaoDigital:Curso {nome: 'Transformação Digital', tipo: 'Pós-Graduação'}),

    (pg_FisioterapiaDesportoDesporto:Curso {nome: 'Fisioterapia no Desporto', tipo: 'Pós-Graduação'}),
    (pg_TreinoAltoRendimento:Curso {nome: 'Treino de Alto Rendimento Desportivo', tipo: 'Pós-Graduação'}),
    (pg_TreinoPersonalizado:Curso {nome: 'Treino Personalizado e Exercício Clínico', tipo: 'Pós-Graduação'});


// Criar nós para Formação Avançada
CREATE 
    (fa_AmbientesHibridos:Curso {nome: 'Ambientes Híbridos com Recurso a Metodologias Ativas: Aprendizagem Invertida e Gamificação', tipo: 'Formação Avançada'}),
    (fa_AtividadesFisicas:Curso {nome: 'Atividades Físicas de Exploração da Natureza — Uma Perspetiva Formativa Ecológica', tipo: 'Formação Avançada'}),
    (fa_FormacaoFormadores:Curso {nome: 'Curso de Formação de Formadores em Ambientes Virtuais de Aprendizagem em Contexto Prisional', tipo: 'Formação Avançada'}),
    (fa_Profissionalizacao:Curso {nome: 'Curso de Profissionalização em Serviço', tipo: 'Formação Avançada'}),
    (fa_CursoAcupunctores:Curso {nome: 'Curso para Acupunctores com Cédula Provisória', tipo: 'Formação Avançada'}),
    (fa_InglesCFS110:Curso {nome: 'Ensino de Inglês no 1.º Ciclo do Ensino Básico - CFS 110', tipo: 'Formação Avançada'}),
    (fa_InglesCFS220:Curso {nome: 'Ensino de Inglês no 1.º Ciclo do Ensino Básico - CFS 220', tipo: 'Formação Avançada'}),
    (fa_InglesCFS330:Curso {nome: 'Ensino de Inglês no 1.º Ciclo do Ensino Básico - CFS 330', tipo: 'Formação Avançada'}),
    (fa_GestaoProjetosCulturais:Curso {nome: 'Gestão de Projetos Culturais', tipo: 'Formação Avançada'}),
    (fa_Imagiologia:Curso {nome: 'Imagiologia aplicada à fisioterapia', tipo: 'Formação Avançada'}),
    (fa_MatematicaRecreativa:Curso {nome: 'Matemática Recreativa: Jogos, Magia e Outras Atividades “Fora Da Caixa”', tipo: 'Formação Avançada'}),
    (fa_MetodologiaGinastica:Curso {nome: 'Metodologia Criativa na Abordagem da Ginástica em Educação Pré-Escolar e no 1.º Ciclo do Ensino Básico', tipo: 'Formação Avançada'}),
    (fa_MetodologiasAtivas:Curso {nome: 'Metodologias Ativas — Aprendizagem Mediada por Tecnologias', tipo: 'Formação Avançada'}),
    (fa_MusicaEscola:Curso {nome: 'Música na Escola. A Abrir', tipo: 'Formação Avançada'}),
    (fa_MusicaSignificativa:Curso {nome: 'Música Significativa', tipo: 'Formação Avançada'}),
    (fa_PerturbacaoCoordenacao:Curso {nome: 'Perturbação do Desenvolvimento da Coordenação em Contexto Escolar: Da Identificação à Intervenção', tipo: 'Formação Avançada'}),
    (fa_PartiturasDigitais:Curso {nome: 'Plataformas Digitais de Edição de Partituras', tipo: 'Formação Avançada'});





    // Criar relações para Pós-Graduações de Saúde
MATCH (pg:Curso {tipo: 'Pós-Graduação'}) 
WHERE pg.nome IN ['Enfermagem de Bloco Operatório: Enfermagem de Anestesia',
                   'Enfermagem de Bloco Operatório: Instrumentação Cirúrgica',
                   'Enfermagem de Bloco Operatório: Instrumentação Cirúrgica e Enfermagem de Anestesia',
                   'Enfermagem do Trabalho',
                   'Enfermagem em Reprocessamento de Dispositivos',
                   'Enfermagem em Reprocessamento de Dispositivos e em Prevenção e Controlo de Infeção e Resistência aos Antimicrobianos',
                   'Fisioterapia no Desporto',
                   'Geronto-geriatria',
                   'Prevenção e Controlo de Infeção e Resistência aos Antimicrobianos',
                   'Psicologia da Saúde Ocupacional',
                   'Saúde Pública e Gestão da Qualidade Alimentar',
                   'Supervisão Clínica na Formação e Desenvolvimento Profissional de Enfermeiros',
                   'Supervisão Clínica para Enfermeiros',
                   'Supervisão Clínica para Profissionais de Saúde',
                   'Termalismo, Turismo e SPA']
MERGE (pg)-[:PERTENCE_A]->(:Area {nome: 'Saúde'})

// Criar relações para Pós-Graduações de Gestão e Administração
MATCH (pg:Curso {tipo: 'Pós-Graduação'}) 
WHERE pg.nome IN ['Administração e Gestão de Unidades de Saúde',
                   'Administração e Gestão de Unidades de Saúde e Gestão de Recursos Humanos',
                   'Administração Escolar',
                   'Bibliotecas Escolares — Gestão e Animação',
                   'Gestão de Recursos Humanos',
                   'Gestão de Serviços de Economia Social',
                   'Gestão e Administração Escolar',
                   'Gestão Estratégica de Recursos Humanos',
                   'Gestão Estratégica de Recursos Humanos e Gestão de Serviços de Economia Social',
                   'Inovação, Gestão da Qualidade e Auditoria em Saúde',
                   'Liderança e Negócios',
                   'Relações Internacionais — A Nova (des)Ordem Mundial: Abordagens Regionais para a Paz e os Conflitos',
                   'Saúde Pública e Gestão da Qualidade Alimentar']
MERGE (pg)-[:PERTENCE_A]->(:Area {nome: 'Gestão e Administração'})

// Criar relações para Pós-Graduações de Educação
MATCH (pg:Curso {tipo: 'Pós-Graduação'}) 
WHERE pg.nome IN ['Bibliotecas Escolares — Gestão e Animação',
                   'Docência no Ensino Superior',
                   'Educação em Creche — Intervenção e Animação Educativa',
                   'Educação Especial: Domínio Cognitivo e Motor',
                   'Educação Especial: Domínio da Audição e Surdez',
                   'Educação Especial: Domínio da Baixa Visão e Cegueira',
                   'Educação Especial: Domínio da Intervenção Precoce na Infância',
                   'Intervenção Comunitária',
                   'Português Língua Não Materna',
                   'Supervisão Pedagógica e Avaliação em Educação']
MERGE (pg)-[:PERTENCE_A]->(:Area {nome: 'Educação'})

// Criar relações para Pós-Graduações de Tecnologia
MATCH (pg:Curso {tipo: 'Pós-Graduação'}) 
WHERE pg.nome IN ['Cibersegurança e Proteção de Dados na Administração Pública',
                   'Tecnologias de Informação e Comunicação: Ecossistemas Híbridos de Aprendizagem',
                   'Transformação Digital']
MERGE (pg)-[:PERTENCE_A]->(:Area {nome: 'Tecnologia'})

// Criar relações para Pós-Graduações de Desporto
MATCH (pg:Curso {tipo: 'Pós-Graduação'}) 
WHERE pg.nome IN ['Fisioterapia no Desporto',
                   'Treino de Alto Rendimento Desportivo',
                   'Treino Personalizado e Exercício Clínico']
MERGE (pg)-[:PERTENCE_A]->(:Area {nome: 'Desporto'})

