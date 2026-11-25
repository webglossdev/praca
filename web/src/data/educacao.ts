// SPDX-License-Identifier: AGPL-3.0-or-later

import type { Poder } from "./pessoas";

export interface FonteEducacional {
  orgao: string;
  documento: string;
  url: string;
  coletado_em: string;
  licenca: string;
}

export type EsferaId = "municipio" | "estado" | "uniao";

export interface EsferaFederativa {
  id: EsferaId;
  nome: string;
  subtitulo: string;
  executivo: string;
  legislativo: string;
  impostosProprios: string[];
  transferenciasPrincipais: string[];
  responsabilidadesPrincipais: string[];
  quemFiscaliza: string;
  fonte: FonteEducacional;
}

export interface SituacaoCotidiana {
  id: string;
  pergunta: string;
  categoria: string;
  esfera: EsferaId | "compartilhada";
  esferaLabel: string;
  poderPrincipal: Poder | "multiplo";
  quemExecuta: string;
  quemFiscaliza: string;
  comoCobrar: string;
  palavrasChave: string;
  fonte: FonteEducacional;
}

export interface EtapaCicloLei {
  ordem: string;
  titulo: string;
  resumo: string;
  detalhePratico: string;
  fonte: FonteEducacional;
}

export interface TipoProposicao {
  sigla: string;
  nome: string;
  paraQueServe: string;
  quorumAprovacao: string;
  temSancaoPresidencial: string;
  fonte: FonteEducacional;
}

export interface PilarOrcamento {
  id: string;
  sigla: string;
  titulo: string;
  resumo: string;
  naPratica: string;
  fonte: FonteEducacional;
}

export interface RegraEleitoral {
  id: string;
  titulo: string;
  resumo: string;
  comoFunciona: string[];
  fonte: FonteEducacional;
}

export interface CanalCidadao {
  id: string;
  titulo: string;
  categoria: "Propor leis" | "Reclamar e pedir dados" | "Fiscalizar e denunciar" | "Acompanhar direto";
  orgao: string;
  paraQueServe: string;
  passoAPasso: string[];
  prazoOuRegra: string;
  url: string;
  rotuloLink: string;
  fonte: FonteEducacional;
}

export type CategoriaGlossario =
  | "legislativo"
  | "orcamento"
  | "eleicoes"
  | "justica"
  | "cidadania";

export interface TermoGlossario {
  slug: string;
  termo: string;
  categoria: CategoriaGlossario;
  categoriaLabel: string;
  emUmaFrase: string;
  explicacao: string;
  exemploPratico: string;
  fonte: FonteEducacional;
}

export interface GuiaPoder {
  id: Poder;
  nome: string;
  corNome: string;
  quemIntegra: string;
  missaoConstitucional: string;
  oQueFaz: string[];
  oQueNaoFaz: string[];
  comoFiscalizar: string;
  fonte: FonteEducacional;
}

const DATA_COLETA = "2026-11-14";

const FONTES = {
  cf88: {
    orgao: "Constituição Federal (Planalto)",
    documento: "Constituição da República Federativa do Brasil de 1988",
    url: "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm",
    coletado_em: DATA_COLETA,
    licenca: "ato oficial / domínio público (Art. 8º, IV, Lei 9.610/98)",
  },
  camara: {
    orgao: "Câmara dos Deputados",
    documento: "Portal Institucional e Processo Legislativo",
    url: "https://www.camara.leg.br/",
    coletado_em: DATA_COLETA,
    licenca: "dados públicos; termos da fonte",
  },
  senadoEcidadania: {
    orgao: "Senado Federal",
    documento: "Portal e-Cidadania",
    url: "https://www12.senado.leg.br/ecidadania/",
    coletado_em: DATA_COLETA,
    licenca: "dados públicos; termos da fonte",
  },
  senadoOrcamento: {
    orgao: "Senado Federal / Tesouro Transparente",
    documento: "Orçamento Público (PPA, LDO, LOA) e Transferências",
    url: "https://www.tesourotransparente.gov.br/",
    coletado_em: DATA_COLETA,
    licenca: "dados públicos; termos da fonte",
  },
  tse: {
    orgao: "Tribunal Superior Eleitoral (TSE)",
    documento: "Sistema Eleitoral, Urna Eletrônica e Boletim de Urna",
    url: "https://www.tse.jus.br/",
    coletado_em: DATA_COLETA,
    licenca: "dados públicos; termos da fonte",
  },
  falaBr: {
    orgao: "Controladoria-Geral da União (CGU)",
    documento: "Plataforma Fala.BR e Lei de Acesso à Informação (Lei 12.527/2011)",
    url: "https://falabr.cgu.gov.br/",
    coletado_em: DATA_COLETA,
    licenca: "serviço público oficial",
  },
  stf: {
    orgao: "Supremo Tribunal Federal (STF)",
    documento: "Atribuições Constitucionais e Glossário Jurídico",
    url: "https://www.stf.jus.br/",
    coletado_em: DATA_COLETA,
    licenca: "dados públicos; termos da fonte",
  },
  mpf: {
    orgao: "Ministério Público Federal (MPF)",
    documento: "Sala de Atendimento ao Cidadão",
    url: "https://www.mpf.mp.br/servicos",
    coletado_em: DATA_COLETA,
    licenca: "serviço público oficial",
  },
  tcu: {
    orgao: "Tribunal de Contas da União (TCU)",
    documento: "Portal do Cidadão e Canal de Denúncias",
    url: "https://portal.tcu.gov.br/denuncie",
    coletado_em: DATA_COLETA,
    licenca: "serviço público oficial",
  },
} as const satisfies Record<string, FonteEducacional>;

export const esferasFederativas: EsferaFederativa[] = [
  {
    id: "municipio",
    nome: "Município",
    subtitulo: "A política mais perto da sua porta (5.570 municípios no Brasil)",
    executivo: "Prefeito(a), Vice-Prefeito(a) e Secretários Municipais",
    legislativo: "Câmara Municipal (Vereadores — fiscalizam o prefeito e votam leis locais)",
    impostosProprios: ["IPTU (imóvel urbano)", "ISS (serviços)", "ITBI (compra/venda de imóveis)"],
    transferenciasPrincipais: [
      "FPM (Fundo de Participação dos Municípios, vindo da União)",
      "Cota-parte de ICMS e IPVA repassada pelo Estado",
      "Repasses vinculados de Saúde (SUS) e Educação (FUNDEB)",
    ],
    responsabilidadesPrincipais: [
      "Zeladoria urbana: asfalto de ruas locais, calçadas, poda, coleta de lixo e iluminação pública",
      "Atenção básica à saúde: postos de saúde (UBS), vacinação e UPAs municipais",
      "Educação infantil (creches e pré-escola) e Ensino Fundamental (1º ao 9º ano)",
      "Transporte coletivo intramunicipal, trânsito urbano e Plano Diretor da cidade",
    ],
    quemFiscaliza: "Câmara de Vereadores, Tribunal de Contas (TCE ou TCM) e Ministério Público Estadual",
    fonte: FONTES.cf88,
  },
  {
    id: "estado",
    nome: "Estado e Distrito Federal",
    subtitulo: "Segurança nas ruas, hospitais regionais e Ensino Médio (26 Estados + DF)",
    executivo: "Governador(a), Vice-Governador(a) e Secretários Estaduais",
    legislativo: "Assembleia Legislativa / Deputados Estaduais (ou Câmara Legislativa / Distritais no DF)",
    impostosProprios: ["ICMS (circulação de mercadorias e energia/comunicação)", "IPVA (veículos)", "ITCMD (heranças e doações)"],
    transferenciasPrincipais: [
      "FPE (Fundo de Participação dos Estados)",
      "Repasses federais do SUS e convênios de infraestrutura/segurança",
    ],
    responsabilidadesPrincipais: [
      "Segurança pública estadual: Polícia Militar (ostensiva), Polícia Civil (investigação) e Bombeiros",
      "Hospitais estaduais, centros de especialidades médicas e cirurgias de média/alta complexidade",
      "Ensino Médio público estadual e universidades estaduais",
      "Rodovias estaduais, transporte intermunicipal/metropolitano (ex.: trens/metrôs estaduais) e sistema prisional",
    ],
    quemFiscaliza: "Assembleia Legislativa, Tribunal de Contas do Estado (TCE) e Ministério Público Estadual",
    fonte: FONTES.cf88,
  },
  {
    id: "uniao",
    nome: "União (Governo Federal)",
    subtitulo: "Leis nacionais, macroeconomia, moeda e defesa do país",
    executivo: "Presidente da República, Vice-Presidente, Ministérios e autarquias federais",
    legislativo: "Congresso Nacional: Câmara dos Deputados (513) e Senado Federal (81)",
    impostosProprios: [
      "IRPF e IRPJ (Imposto de Renda)",
      "IPI, PIS/COFINS, CSLL, IOF e Imposto de Importação/Exportação (em transição parcial pela Reforma Tributária)",
      "Contribuições previdenciárias (INSS)",
    ],
    transferenciasPrincipais: [
      "Arrecada a maior fatia tributária e redistribui parte via FPM, FPE, SUS, FUNDEB e transferências diretas",
    ],
    responsabilidadesPrincipais: [
      "Regras econômicas e monetárias: orçamento federal, dívida pública e metas de inflação/juros (Banco Central)",
      "Leis de alcance nacional: Códigos Penal, Civil, Eleitoral e Trabalhista (CLT)",
      "Universidades e Institutos Federais, ENEM/Prouni/FIES e pesquisa científica nacional",
      "Previdência (INSS), Forças Armadas, Polícia Federal, rodovias federais (PRF) e relações exteriores",
    ],
    quemFiscaliza: "Congresso Nacional, Tribunal de Contas da União (TCU), CGU, STF e Ministério Público Federal",
    fonte: FONTES.cf88,
  },
];

export const situacoesCotidianas: SituacaoCotidiana[] = [
  {
    id: "buraco-iluminacao",
    pergunta: "Buraco na rua, lixo acumulado ou poste apagado no bairro",
    categoria: "Zeladoria urbana",
    esfera: "municipio",
    esferaLabel: "Município",
    poderPrincipal: "executivo",
    quemExecuta: "Prefeitura Municipal (Secretaria de Obras, Conservação ou Energia).",
    quemFiscaliza: "Vereadores da Câmara Municipal e Ouvidoria da Prefeitura.",
    comoCobrar: "Abra protocolo na ouvidoria municipal (ex.: 1746, 156 ou portal da prefeitura) e envie o número de protocolo ao gabinete de vereadores da sua região.",
    palavrasChave: "buraco rua asfalto calcada lixo iluminacao poste arvore poda prefeitura zeladoria",
    fonte: FONTES.cf88,
  },
  {
    id: "posto-saude-ubs",
    pergunta: "Falta de médico ou remédio básico no posto de saúde (UBS) ou UPA",
    categoria: "Saúde básica",
    esfera: "municipio",
    esferaLabel: "Município (com repasses do SUS)",
    poderPrincipal: "executivo",
    quemExecuta: "Secretaria Municipal de Saúde, gerenciando postos (UBS) e UPAs com cofinanciamento estadual e federal do SUS.",
    quemFiscaliza: "Câmara de Vereadores, Conselho Municipal de Saúde e Ministério Público Estadual.",
    comoCobrar: "Registre falta de medicamento ou atendimento na Ouvidoria do SUS (136) e na ouvidoria da Secretaria Municipal de Saúde.",
    palavrasChave: "medico remedio posto saude ubs upa prefeitura sus fila consulta",
    fonte: FONTES.cf88,
  },
  {
    id: "hospital-cirurgia",
    pergunta: "Hospital estadual lotado ou espera longa por cirurgia de alta complexidade",
    categoria: "Saúde especializada",
    esfera: "estado",
    esferaLabel: "Estado (SUS)",
    poderPrincipal: "executivo",
    quemExecuta: "Secretaria Estadual de Saúde, responsável por hospitais regionais/estaduais e centrais de regulação de leitos.",
    quemFiscaliza: "Assembleia Legislativa (Deputados Estaduais), TCE, Ministério Público Estadual e Defensoria Pública.",
    comoCobrar: "Registre na Ouvidoria Geral do Estado e na Ouvidoria do SUS; em urgências negadas, acione a Defensoria Pública ou o Ministério Público.",
    palavrasChave: "hospital estadual cirurgia alta complexidade leito uti governador sus",
    fonte: FONTES.cf88,
  },
  {
    id: "creche-fundamental",
    pergunta: "Vaga em creche ou qualidade da escola municipal (1º ao 9º ano)",
    categoria: "Educação básica",
    esfera: "municipio",
    esferaLabel: "Município",
    poderPrincipal: "executivo",
    quemExecuta: "Prefeitura (Secretaria Municipal de Educação), conforme Art. 211, § 2º da Constituição.",
    quemFiscaliza: "Câmara Municipal, Conselho do FUNDEB e Ministério Público.",
    comoCobrar: "Protocole pedido formal na Secretaria Municipal de Educação; a matrícula em creche/pré-escola e ensino fundamental é direito constitucional.",
    palavrasChave: "creche escola municipal ensino fundamental professor merenda educacao",
    fonte: FONTES.cf88,
  },
  {
    id: "ensino-medio",
    pergunta: "Infraestrutura ou falta de professores no Ensino Médio público",
    categoria: "Educação média",
    esfera: "estado",
    esferaLabel: "Estado / DF",
    poderPrincipal: "executivo",
    quemExecuta: "Governo Estadual (Secretaria Estadual de Educação), conforme Art. 211, § 3º da Constituição.",
    quemFiscaliza: "Deputados Estaduais na Assembleia Legislativa, TCE e Ministério Público Estadual.",
    comoCobrar: "Acione a Ouvidoria da Secretaria Estadual de Educação e a Comissão de Educação da Assembleia Legislativa.",
    palavrasChave: "ensino medio escola estadual colegio estadual professor governador",
    fonte: FONTES.cf88,
  },
  {
    id: "seguranca-pm-pc",
    pergunta: "Policiamento ostensivo nas ruas, assaltos ou investigação de crimes em delegacia",
    categoria: "Segurança pública",
    esfera: "estado",
    esferaLabel: "Estado / DF",
    poderPrincipal: "executivo",
    quemExecuta: "Governo Estadual via Polícia Militar (policiamento ostensivo) e Polícia Civil (investigação e boletins).",
    quemFiscaliza: "Corregedorias das polícias, Ministério Público Estadual (controle externo da atividade policial) e Assembleia Legislativa.",
    comoCobrar: "Registre sempre o Boletim de Ocorrência (orienta alocação de viaturas) e cobre o Governador e Deputados Estaduais pelo orçamento e efetivo; atenção: mudar penas e leis penais depende do Congresso Nacional (União).",
    palavrasChave: "policia militar civil delegacia seguranca assalto crime governador",
    fonte: FONTES.cf88,
  },
  {
    id: "onibus-metro-estrada",
    pergunta: "Linha de ônibus no bairro vs. metrô, trem ou rodovia entre cidades",
    categoria: "Mobilidade e estradas",
    esfera: "compartilhada",
    esferaLabel: "Município (local) · Estado (intermunicipal) · União (BRs)",
    poderPrincipal: "executivo",
    quemExecuta: "Prefeitura gerencia ônibus e ruas dentro do município; Estado gerencia linhas intermunicipais/metrôs e rodovias estaduais; União gerencia rodovias federais (BRs).",
    quemFiscaliza: "Agências reguladoras de transporte, Câmaras Municipais, Assembleias Legislativas ou ANTT/TCU (no âmbito federal).",
    comoCobrar: "Verifique se a linha liga pontos dentro de uma cidade (Prefeitura) ou cruza municípios (Estado), ou se a rodovia começa com 'BR' (DNIT/União).",
    palavrasChave: "onibus metro trem tarifa passagem transito rodovia br estrada",
    fonte: FONTES.cf88,
  },
  {
    id: "lei-penal-eleitoral-clt",
    pergunta: "Mudar regras do Código Penal, leis trabalhistas (CLT) ou regras das eleições",
    categoria: "Legislação nacional",
    esfera: "uniao",
    esferaLabel: "União (Congresso Nacional)",
    poderPrincipal: "legislativo",
    quemExecuta: "Deputados Federais e Senadores debatem e votam leis federais (Art. 22 da CF); Presidente sanciona ou veta.",
    quemFiscaliza: "Sociedade civil, imprensa e STF (que julga se a nova lei respeita a Constituição).",
    comoCobrar: "Participe da consulta pública no e-Cidadania/Câmara e cobre os deputados federais e senadores eleitos pelo seu estado.",
    palavrasChave: "codigo penal crime pena trabalhista clt eleicao lei federal congresso deputado senador",
    fonte: FONTES.cf88,
  },
  {
    id: "inss-juros-universidade",
    pergunta: "Aposentadoria do INSS, salário mínimo, taxa de juros (Selic) ou Universidade Federal",
    categoria: "Políticas nacionais",
    esfera: "uniao",
    esferaLabel: "União",
    poderPrincipal: "executivo",
    quemExecuta: "Governo Federal (Ministérios, INSS, MEC) e, na taxa básica de juros, o Banco Central com mandato autônomo.",
    quemFiscaliza: "Congresso Nacional, TCU, CGU e Ministério Público Federal.",
    comoCobrar: "Para benefícios e serviços federais, use o portal Gov.br ou abra protocolo e pedido LAI na plataforma Fala.BR.",
    palavrasChave: "inss aposentadoria salario minimo juros selic banco central enem universidade federal",
    fonte: FONTES.falaBr,
  },
  {
    id: "impostos-quem-cobra",
    pergunta: "Saber para onde vão IPTU, IPVA, ICMS e Imposto de Renda",
    categoria: "Tributos",
    esfera: "compartilhada",
    esferaLabel: "Município (IPTU/ISS) · Estado (IPVA/ICMS) · União (IR)",
    poderPrincipal: "multiplo",
    quemExecuta: "Cada ente arrecada seus impostos próprios; parte do ICMS/IPVA estadual vai para os municípios e parte do IR/IPI federal volta via FPM e FPE.",
    quemFiscaliza: "Portais da Transparência municipais, estaduais e federal + Tribunais de Contas.",
    comoCobrar: "Consulte o Portal da Transparência do ente arrecadador e peça contratos detalhados via LAI se faltarem dados.",
    palavrasChave: "imposto iptu ipva icms iss imposto de renda tributo taxa prefeitura estado",
    fonte: FONTES.senadoOrcamento,
  },
  {
    id: "desvio-verba-obra",
    pergunta: "Suspeita de obra parada, licitação irregular ou desvio de dinheiro público",
    categoria: "Controle e fiscalização",
    esfera: "compartilhada",
    esferaLabel: "União, Estado ou Município (conforme a origem da verba)",
    poderPrincipal: "judiciario",
    quemExecuta: "Controle interno (CGU/controladorias), Controle externo (TCU/TCE/TCM) e investigação pelo Ministério Público e Polícias.",
    quemFiscaliza: "Qualquer cidadão pode provocar a fiscalização com fatos e documentos públicos.",
    comoCobrar: "Reúna o número do contrato/convênio no Portal da Transparência e denuncie na Fala.BR (verba federal), TCU ou Ministério Público.",
    palavrasChave: "corrupcao desvio verba obra parada licitacao fraude denuncia tcu mpf cgu",
    fonte: FONTES.tcu,
  },
  {
    id: "direitos-constitucionais",
    pergunta: "Decisões sobre se uma lei ou ato do governo viola a Constituição",
    categoria: "Justiça constitucional",
    esfera: "uniao",
    esferaLabel: "União (Poder Judiciário · STF)",
    poderPrincipal: "judiciario",
    quemExecuta: "O Supremo Tribunal Federal (STF) julga ações diretas de constitucionalidade e recursos extraordinários com repercussão geral.",
    quemFiscaliza: "Sessões públicas com voto fundamentado, TV Justiça e controle social; crimes de responsabilidade dos ministros competem ao Senado.",
    comoCobrar: "Acompanhe as pautas e votos completos no portal do STF e transmissões oficiais sem recortes descontextualizados.",
    palavrasChave: "stf constituicao supremo julgamento lei inconstitucional liminar adpf adi",
    fonte: FONTES.stf,
  },
];

export const etapasCicloLei: EtapaCicloLei[] = [
  {
    ordem: "01",
    titulo: "Iniciativa (quem pode propor)",
    resumo: "Deputados federais, senadores, Presidente da República, tribunais superiores, PGR e cidadãos (via Iniciativa Popular).",
    detalhePratico: "Um cidadão também pode começar uma ideia pelo Portal e-Cidadania: com 20 mil apoios em 4 meses, ela vira Sugestão Legislativa debatida no Senado.",
    fonte: FONTES.cf88,
  },
  {
    ordem: "02",
    titulo: "Comissões temáticas e Relatoria",
    resumo: "Antes do Plenário, o projeto passa por comissões técnicas (Saúde, Educação, Segurança etc.).",
    detalhePratico: "O presidente da comissão escolhe um Relator, que é quem escreve o parecer e pode propor um texto substitutivo. Muitos PLs comuns são decididos nas próprias comissões ('poder conclusivo') sem ir ao Plenário, salvo recurso.",
    fonte: FONTES.camara,
  },
  {
    ordem: "03",
    titulo: "CCJ e impacto no orçamento",
    resumo: "Comissão de Constituição e Justiça (CCJ) checa se o projeto não fere a Constituição; comissão de Finanças avalia o custo.",
    detalhePratico: "Se o projeto cria gasto público sem apontar fonte de receita (exigência da Lei de Responsabilidade Fiscal e da CF), ele pode ser travado antes de ir a voto.",
    fonte: FONTES.camara,
  },
  {
    ordem: "04",
    titulo: "Votação nas duas Casas (Bicameralismo)",
    resumo: "O texto aprovado na Casa iniciadora (geralmente a Câmara) vai para revisão na outra Casa (Senado).",
    detalhePratico: "Se o Senado alterar o mérito do projeto, o texto volta para a Câmara decidir se aceita as mudanças ou retoma o texto anterior.",
    fonte: FONTES.cf88,
  },
  {
    ordem: "05",
    titulo: "Sanção ou Veto presidencial",
    resumo: "O Presidente tem 15 dias úteis para sancionar (virar lei) ou vetar trechos ou o texto inteiro.",
    detalhePratico: "Veto não é palavra final: deputados e senadores podem derrubar o veto em sessão conjunta do Congresso por maioria absoluta (257 deputados + 41 senadores). PECs não passam por sanção presidencial.",
    fonte: FONTES.cf88,
  },
  {
    ordem: "06",
    titulo: "Publicação no DOU e controle no STF",
    resumo: "A lei entra em vigor após publicação no Diário Oficial da União (respeitando eventual prazo de adaptação).",
    detalhePratico: "Mesmo depois de sancionada, partidos, entidades nacionais, o PGR, o Presidente ou governadores podem pedir ao STF que verifique se a lei respeita a Constituição.",
    fonte: FONTES.stf,
  },
];

export const tiposProposicao: TipoProposicao[] = [
  {
    sigla: "PL",
    nome: "Projeto de Lei Ordinária",
    paraQueServe: "Cria ou altera a maioria das leis do país (código de trânsito, benefícios, políticas públicas).",
    quorumAprovacao: "Maioria simples (metade + 1 dos presentes, desde que haja quórum mínimo na sessão).",
    temSancaoPresidencial: "Sim (15 dias úteis para sancionar ou vetar).",
    fonte: FONTES.camara,
  },
  {
    sigla: "PLP",
    nome: "Projeto de Lei Complementar",
    paraQueServe: "Regulamenta temas que a própria Constituição exige lei especial (ex.: regras fiscais, impostos, Lei da Ficha Limpa).",
    quorumAprovacao: "Maioria absoluta (pelo menos 257 deputados e 41 senadores).",
    temSancaoPresidencial: "Sim (15 dias úteis para sancionar ou vetar).",
    fonte: FONTES.cf88,
  },
  {
    sigla: "PEC",
    nome: "Proposta de Emenda à Constituição",
    paraQueServe: "Altera o próprio texto da Constituição Federal (reformas tributária, previdenciária, regras eleitorais constitucionais).",
    quorumAprovacao: "3/5 dos votos em 2 turnos em cada Casa (308 deputados + 49 senadores).",
    temSancaoPresidencial: "Não. Se aprovada nas duas Casas, é promulgada diretamente pelo Congresso.",
    fonte: FONTES.cf88,
  },
  {
    sigla: "MP",
    nome: "Medida Provisória",
    paraQueServe: "Editada pelo Presidente em caso de relevância e urgência, com força de lei imediata.",
    quorumAprovacao: "Vale por 60 dias (prorrogáveis por mais 60); perde eficácia se Câmara e Senado não aprovarem conversão em lei.",
    temSancaoPresidencial: "Só há sanção/veto se o Congresso aprovar mudanças no texto original da MP.",
    fonte: FONTES.cf88,
  },
];

export const pilaresOrcamento: PilarOrcamento[] = [
  {
    id: "ppa-ldo-loa",
    sigla: "PPA · LDO · LOA",
    titulo: "As três leis que comandam o dinheiro público",
    resumo: "Nenhum gasto público legal acontece sem autorização prévia no ciclo orçamentário.",
    naPratica: "O PPA planeja prioridades para 4 anos; a LDO define anualmente as regras, metas fiscais e o que pode ganhar prioridade; a LOA é a lista detalhada de quanto se estima arrecadar e gastar no ano seguinte.",
    fonte: FONTES.senadoOrcamento,
  },
  {
    id: "rigidez",
    sigla: "Obrigatórias × Discricionárias",
    titulo: "Por que o orçamento é quase todo engessado",
    resumo: "Mais de 90% das despesas primárias da União já chegam comprometidas por lei ou pela Constituição.",
    naPratica: "Previdência Social (INSS), salários do funcionalismo, benefícios legais (BPC, Bolsa Família) e pisos mínimos de Saúde e Educação têm prioridade obrigatória. Sobra menos de 10% para investimentos livres e manutenção de estradas, prédios e equipamentos.",
    fonte: FONTES.senadoOrcamento,
  },
  {
    id: "emendas",
    sigla: "Emendas (RP 6, 7 e 8)",
    titulo: "O dinheiro que deputados e senadores direcionam",
    resumo: "Emendas individuais e de bancada passaram a ser impositivas (o Executivo é obrigado a executar dentro dos limites constitucionais).",
    naPratica: "Metade das emendas individuais precisa ir obrigatoriamente para a Saúde (Art. 166, § 9º da CF). Transferências especiais ('emendas Pix') exigem planos de trabalho, rastreabilidade e fiscalização dos órgãos de controle.",
    fonte: FONTES.cf88,
  },
  {
    id: "fpm-fpe",
    sigla: "FPM e FPE",
    titulo: "Como o dinheiro volta de Brasília para sua cidade",
    resumo: "A União concentra a maior parte da arrecadação e transfere fatias obrigatórias aos estados e municípios.",
    naPratica: "A maioria dos 5.570 municípios brasileiros não arrecada IPTU/ISS suficiente para se manter e depende diretamente do Fundo de Participação dos Municípios (FPM), calculado conforme faixas populacionais.",
    fonte: FONTES.senadoOrcamento,
  },
];

export const regrasEleitorais: RegraEleitoral[] = [
  {
    id: "majoritaria-proporcional",
    titulo: "Majoritária × Proporcional: por que um candidato com menos votos pode se eleger",
    resumo: "No Brasil convivem dois sistemas eleitorais diferentes na mesma eleição.",
    comoFunciona: [
      "Eleição majoritária (Presidente, Governador, Prefeito e Senador): vence quem tiver mais votos válidos (com 2º turno se ninguém passar de 50% dos válidos em Presidente, Governador e cidades com mais de 200 mil eleitores).",
      "Eleição proporcional (Deputados Federais, Estaduais, Distritais e Vereadores): as vagas são divididas primeiro entre partidos e federações usando o Quociente Eleitoral (votos válidos ÷ vagas), e só depois vão para os mais votados de cada partido que atingiu votos mínimos individuais.",
    ],
    fonte: FONTES.tse,
  },
  {
    id: "fidelidade-clausula",
    titulo: "Fidelidade partidária, federações e cláusula de desempenho",
    resumo: "Regras que moldam quantos partidos existem e para quem pertence o mandato.",
    comoFunciona: [
      "Fidelidade partidária: em cargos proporcionais, o mandato pertence ao partido/federação. Trocar de sigla fora da janela partidária (30 dias, 6 meses antes do pleito) pode levar à perda do mandato, salvo justa causa prevista na Constituição.",
      "Federação partidária: partidos que se unem por no mínimo 4 anos funcionando como uma única bancada nacional (diferente de coligação, que deixou de valer em eleições proporcionais).",
      "Cláusula de barreira (desempenho): exige percentual mínimo de votos nacionais ou deputados distribuídos pelos estados para que o partido tenha direito ao Fundo Partidário e ao tempo gratuito de rádio e TV.",
    ],
    fonte: FONTES.tse,
  },
  {
    id: "urna-auditoria",
    titulo: "Segurança e auditoria da Urna Eletrônica",
    resumo: "Como funciona a verificação física e digital antes, durante e após a votação.",
    comoFunciona: [
      "Desconectada de rede: a urna eletrônica não possui modem de internet, Wi-Fi ou Bluetooth; os dados são gravados em mídia física assinada criptograficamente.",
      "Antes da eleição: partidos, OAB, MP, Polícia Federal e universidades acompanham o código-fonte 1 ano antes e há o Teste Público de Segurança (TPS) no TSE.",
      "No dia da votação: às 7h imprime-se a 'zerésima' provando zero votos registrados; às 17h imprime-se o Boletim de Urna (BU) na porta da seção com QR Code que qualquer cidadão pode escanear e comparar depois com os números publicados no portal do TSE.",
    ],
    fonte: FONTES.tse,
  },
];

export const canaisCidadao: CanalCidadao[] = [
  {
    id: "ecidadania",
    titulo: "Portal e-Cidadania (Senado Federal)",
    categoria: "Propor leis",
    orgao: "Senado Federal",
    paraQueServe: "Propor uma nova lei ('Ideia Legislativa'), opinar contra ou a favor em projetos em tramitação e enviar perguntas em audiências ao vivo.",
    passoAPasso: [
      "Entre com sua conta no portal oficial do e-Cidadania.",
      "Em 'Ideia Legislativa', descreva de forma clara e objetiva o problema e a mudança legal proposta.",
      "Se conseguir 20.000 apoios de outros cidadãos em até 4 meses, a ideia vira Sugestão Legislativa formal e passa a ser debatida por Senadores na Comissão de Direitos Humanos e Legislação Participativa (CDH).",
    ],
    prazoOuRegra: "20.000 apoios em 4 meses tornam a pauta obrigatória em comissão.",
    url: "https://www12.senado.leg.br/ecidadania/",
    rotuloLink: "Acessar e-Cidadania",
    fonte: FONTES.senadoEcidadania,
  },
  {
    id: "enquetes-camara",
    titulo: "Enquetes e Participação na Câmara dos Deputados",
    categoria: "Propor leis",
    orgao: "Câmara dos Deputados",
    paraQueServe: "Registrar seu voto de opinião ('Concordo totalmente' até 'Discordo totalmente') nas propostas em debate e consultar contatos oficiais dos 513 deputados.",
    passoAPasso: [
      "Busque o número da proposta (ex.: PL ou PEC) no portal da Câmara.",
      "Abra a ficha de tramitação e acesse o bloco 'Enquete / Opine sobre o projeto'.",
      "Anote quem é o(a) relator(a) e envie argumentos objetivos pelo e-mail institucional oficial do gabinete (dep.nome@camara.leg.br).",
    ],
    prazoOuRegra: "Sinalização oficial contínua durante toda a tramitação do projeto.",
    url: "https://www.camara.leg.br/",
    rotuloLink: "Abrir Portal da Câmara",
    fonte: FONTES.camara,
  },
  {
    id: "falabr-lai",
    titulo: "Fala.BR — Ouvidoria e Lei de Acesso à Informação (LAI)",
    categoria: "Reclamar e pedir dados",
    orgao: "Controladoria-Geral da União (CGU)",
    paraQueServe: "Pedir documentos, planilhas, contratos e explicações oficiais a qualquer órgão do Executivo federal via LAI (Lei nº 12.527/2011) ou registrar reclamações e denúncias.",
    passoAPasso: [
      "Acesse a plataforma Fala.BR com sua conta Gov.br.",
      "Escolha 'Acesso à Informação' para pedir dados públicos (não é obrigatório explicar o motivo do pedido) ou 'Denúncia / Reclamação' para falhas em serviços e irregularidades.",
      "Guarde o número de protocolo e acompanhe o prazo legal de resposta (com direito a recurso se a resposta vier incompleta).",
    ],
    prazoOuRegra: "Prazo legal da LAI: até 20 dias corridos, prorrogáveis por mais 10 mediante justificativa.",
    url: "https://falabr.cgu.gov.br/",
    rotuloLink: "Abrir Fala.BR",
    fonte: FONTES.falaBr,
  },
  {
    id: "ouvidorias-locais",
    titulo: "Ouvidorias Estaduais e Municipais (Zeladoria e Serviços)",
    categoria: "Reclamar e pedir dados",
    orgao: "Prefeituras e Governos Estaduais",
    paraQueServe: "Cobrar problemas concretos da cidade ou do estado (rua, iluminação, posto de saúde, escola estadual, transporte) gerando protocolo auditável.",
    passoAPasso: [
      "Identifique pela Bússola Federativa se o serviço é municipal ou estadual.",
      "Use a central oficial da sua cidade/estado (ex.: 1746 no Rio de Janeiro, SP156 em São Paulo, 162 no DF, ou a Ouvidoria Geral no portal da prefeitura/estado).",
      "Guarde foto com data e número do protocolo: sem resposta no prazo, encaminhe o protocolo à Câmara de Vereadores, Assembleia Legislativa ou Ministério Público.",
    ],
    prazoOuRegra: "Gera protocolo oficial obrigatório para cobrança subsequente.",
    url: "https://www.gov.br/ouvidorias/pt-br",
    rotuloLink: "Rede de Ouvidorias (CGU)",
    fonte: FONTES.falaBr,
  },
  {
    id: "mpf-tcu",
    titulo: "Ministério Público (MPF/MPE) e Tribunais de Contas (TCU/TCE)",
    categoria: "Fiscalizar e denunciar",
    orgao: "MPF · MPE · TCU · TCEs",
    paraQueServe: "Representar formalmente quando houver indício documentado de fraude em licitação, superfaturamento, dano ambiental ou violação de direito coletivo.",
    passoAPasso: [
      "Reúna evidências objetivas (número de licitação, nota fiscal, endereço da obra, fotos datadas ou resposta obtida via LAI).",
      "Para verbas federais ou competências da União, protocole na Sala de Atendimento ao Cidadão do MPF ou no portal de denúncias do TCU.",
      "Para prefeituras e governos estaduais, protocole no Ministério Público Estadual (MPE) e no Tribunal de Contas do respectivo estado.",
    ],
    prazoOuRegra: "Permite acompanhamento processual pelo número do procedimento.",
    url: "https://portal.tcu.gov.br/denuncie",
    rotuloLink: "Canal de Denúncias do TCU",
    fonte: FONTES.tcu,
  },
  {
    id: "mpf-servicos",
    titulo: "Sala de Atendimento ao Cidadão do Ministério Público Federal",
    categoria: "Fiscalizar e denunciar",
    orgao: "Ministério Público Federal (MPF)",
    paraQueServe: "Comunicar ilegalidades envolvendo recursos federais, crimes federais, meio ambiente, direitos do consumidor e tutela coletiva.",
    passoAPasso: [
      "Acesse MPF Serviços com login Gov.br.",
      "Descreva os fatos em ordem cronológica, citando datas, locais e documentos disponíveis.",
      "Acompanhe o andamento da manifestação diretamente pelo sistema.",
    ],
    prazoOuRegra: "Acesso gratuito pela internet para qualquer cidadão.",
    url: "https://www.mpf.mp.br/servicos",
    rotuloLink: "Acessar MPF Serviços",
    fonte: FONTES.mpf,
  },
  {
    id: "acao-popular",
    titulo: "Ação Popular e Projeto de Lei de Iniciativa Popular",
    categoria: "Fiscalizar e denunciar",
    orgao: "Constituição Federal (Art. 5º, LXXIII e Art. 61, § 2º)",
    paraQueServe: "Mecanismos constitucionais diretos: anular na Justiça ato lesivo ao patrimônio público/moralidade (Ação Popular) ou propor lei com assinaturas (Iniciativa Popular).",
    passoAPasso: [
      "Ação Popular: qualquer cidadão com título de eleitor regular (representado por advogado ou Defensoria) pode ingressar contra ato ilegal lesivo ao patrimônio público, histórico ou ambiental.",
      "Iniciativa Popular Federal: exige assinatura de pelo menos 1% do eleitorado nacional distribuído em ao menos 5 estados (ex.: origem da Lei da Ficha Limpa — LC 135/2010).",
      "Municípios e estados preveem versões próprias nas Leis Orgânicas e Constituições Estaduais (geralmente exigindo 5% do eleitorado local).",
    ],
    prazoOuRegra: "Na Ação Popular, o autor fica isento de custas judiciais, salvo comprovada má-fé (Art. 5º, LXXIII CF).",
    url: "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm",
    rotuloLink: "Ler Constituição Federal",
    fonte: FONTES.cf88,
  },
  {
    id: "tvs-publicas",
    titulo: "TV Câmara, TV Senado e TV Justiça (Fontes diretas sem algoritmo)",
    categoria: "Acompanhar direto",
    orgao: "Congresso Nacional e STF",
    paraQueServe: "Assistir sessões plenárias, CPIs, sabatinas e julgamentos na íntegra, lendo o placar real e as falas completas sem cortes enviesados de rede social.",
    passoAPasso: [
      "Nos dias úteis (especialmente terça a quinta), consulte a pauta do Plenário e das principais comissões.",
      "Acompanhe pela TV Câmara, TV Senado ou TV Justiça + na internet.",
      "Compare o discurso no microfone com o voto efetivamente registrado no painel eletrônico.",
    ],
    prazoOuRegra: "Transmissão pública e gratuita das sessões oficiais.",
    url: "https://www.camara.leg.br/ao-vivo",
    rotuloLink: "Câmara Ao Vivo",
    fonte: FONTES.camara,
  },
];

export const glossarioTermos: TermoGlossario[] = [
  {
    slug: "pec",
    termo: "PEC (Proposta de Emenda à Constituição)",
    categoria: "legislativo",
    categoriaLabel: "Legislativo",
    emUmaFrase: "Proposta que muda regras escritas dentro da própria Constituição Federal.",
    explicacao: "Por mexer no texto máximo do país, tem tramitação mais rígida: exige apoio de 3/5 da Câmara (308 votos) e 3/5 do Senado (49 votos) em dois turnos em cada Casa.",
    exemploPratico: "Reformas tributária e previdenciária tramitaram como PEC. Não há veto nem sanção presidencial em PECs.",
    fonte: FONTES.cf88,
  },
  {
    slug: "pl-plp",
    termo: "PL e PLP (Projeto de Lei Ordinária e Complementar)",
    categoria: "legislativo",
    categoriaLabel: "Legislativo",
    emUmaFrase: "As duas vias principais para criar ou alterar leis no Congresso.",
    explicacao: "O PL (lei ordinária) precisa da maioria dos votos dos presentes na sessão. O PLP (lei complementar) exige maioria absoluta de toda a Casa (257 deputados e 41 senadores) e trata de temas reservados pela Constituição.",
    exemploPratico: "A Lei da Ficha Limpa (LC 135/2010) e a Lei de Responsabilidade Fiscal (LC 101/2000) são leis complementares.",
    fonte: FONTES.cf88,
  },
  {
    slug: "medida-provisoria",
    termo: "Medida Provisória (MP)",
    categoria: "legislativo",
    categoriaLabel: "Legislativo",
    emUmaFrase: "Norma editada pelo Presidente com força imediata de lei, mas com prazo de validade.",
    explicacao: "Prevista no Art. 62 da Constituição para situações urgentes e relevantes. Passa a valer no dia da publicação, mas perde validade se o Congresso não votá-la em até 120 dias (60 + 60 dias).",
    exemploPratico: "Criação emergencial de créditos extraordinários ou reajuste imediato do salário mínimo costumam usar MP antes da aprovação definitiva.",
    fonte: FONTES.cf88,
  },
  {
    slug: "relator-e-substitutivo",
    termo: "Relator, Parecer e Substitutivo",
    categoria: "legislativo",
    categoriaLabel: "Legislativo",
    emUmaFrase: "O parlamentar encarregado de analisar um projeto e propor o texto final que vai a voto.",
    explicacao: "Em cada comissão ou no Plenário, o relator estuda o projeto e entrega um parecer (pela aprovação, rejeição ou alteração). Quando modifica substancialmente o projeto original, apresenta um texto chamado 'substitutivo'.",
    exemploPratico: "Cidadãos que querem influenciar um PL procuram saber quem é o relator atual antes de o parecer ser votado.",
    fonte: FONTES.camara,
  },
  {
    slug: "requerimento-urgencia",
    termo: "Requerimento de Urgência",
    categoria: "legislativo",
    categoriaLabel: "Legislativo",
    emUmaFrase: "Atalho regimental que pula a fila das comissões e leva um projeto direto ao Plenário.",
    explicacao: "Aprovada a urgência pelo Plenário, prazos e etapas comuns nas comissões são encurtados, permitindo votar a matéria em poucos dias ou horas.",
    exemploPratico: "Projetos de grande repercussão nacional frequentemente têm urgência votada antes do debate do mérito.",
    fonte: FONTES.camara,
  },
  {
    slug: "cpi",
    termo: "CPI e CPMI (Comissão Parlamentar de Inquérito)",
    categoria: "legislativo",
    categoriaLabel: "Legislativo",
    emUmaFrase: "Comissão criada pelo Legislativo para investigar um fato determinado com poderes próprios de investigação.",
    explicacao: "Uma CPI (em uma Casa) ou CPMI (mista, Câmara + Senado) pode convocar depoentes, requisitar documentos e quebrar sigilos bancário/fiscal/telefônico por decisão fundamentada, mas não julga nem condena: ao fim, encaminha o relatório ao Ministério Público.",
    exemploPratico: "Exige assinatura de pelo menos 1/3 dos membros da Casa e prazo determinado de funcionamento.",
    fonte: FONTES.cf88,
  },
  {
    slug: "ppa-ldo-loa",
    termo: "PPA, LDO e LOA (Ciclo Orçamentário)",
    categoria: "orcamento",
    categoriaLabel: "Orçamento Público",
    emUmaFrase: "O tripé de leis que define onde o dinheiro público será aplicado.",
    explicacao: "O PPA traça o plano estratégico de 4 anos; a LDO estabelece metas e prioridades anuais e orienta o orçamento; a LOA estima as receitas e fixa cada despesa do ano seguinte.",
    exemploPratico: "Nenhuma obra ou programa novo pode receber dinheiro sem previsão na LOA aprovada pelo Legislativo.",
    fonte: FONTES.senadoOrcamento,
  },
  {
    slug: "despesa-obrigatoria-discricionaria",
    termo: "Despesa Obrigatória × Despesa Discricionária",
    categoria: "orcamento",
    categoriaLabel: "Orçamento Público",
    emUmaFrase: "A diferença entre o gasto que o governo é obrigado por lei a pagar e a pequena sobra onde ele escolhe onde investir.",
    explicacao: "Despesas obrigatórias (aposentadorias, folhas salariais, pisos constitucionais de Saúde/Educação) consomem mais de 90% do orçamento primário federal. Despesas discricionárias são o espaço flexível restante para custeio e obras.",
    exemploPratico: "Quando o governo faz um 'contingenciamento' no orçamento, o corte recai quase inteiro sobre despesas discricionárias (como bolsas, manutenção e investimentos).",
    fonte: FONTES.senadoOrcamento,
  },
  {
    slug: "emenda-parlamentar",
    termo: "Emenda Parlamentar (Individual, de Bancada e 'Pix')",
    categoria: "orcamento",
    categoriaLabel: "Orçamento Público",
    emUmaFrase: "Valor do orçamento público que deputados e senadores indicam para obras ou serviços em estados e municípios.",
    explicacao: "Podem ser individuais (de cada parlamentar — 50% obrigatoriamente para a Saúde), de bancada estadual ou de comissão. As chamadas 'emendas Pix' (transferências especiais) vão direto para a conta do estado/município e requerem plano de trabalho e fiscalização.",
    exemploPratico: "A Praça permite acompanhar no perfil de parlamentares quanto cada um indicou e para qual área.",
    fonte: FONTES.cf88,
  },
  {
    slug: "cota-parlamentar",
    termo: "Cota Parlamentar (CEAP / CEAPS)",
    categoria: "orcamento",
    categoriaLabel: "Orçamento Público",
    emUmaFrase: "Verba de reembolso para despesas ligadas ao exercício do mandato parlamentar.",
    explicacao: "Cobre passagens aéreas, aluguel de escritório no estado de origem, combustível, telefonia e divulgação da atividade parlamentar mediante notas fiscais públicas (distinta do salário mensal do deputado/senador).",
    exemploPratico: "Câmara (CEAP) e Senado (CEAPS) publicam nota a nota em dados abertos os valores gastos.",
    fonte: FONTES.camara,
  },
  {
    slug: "fpm",
    termo: "FPM (Fundo de Participação dos Municípios)",
    categoria: "orcamento",
    categoriaLabel: "Orçamento Público",
    emUmaFrase: "Transferência constitucional da União que sustenta a maior parte das prefeituras do país.",
    explicacao: "Formado por parcela da arrecadação federal de Imposto de Renda e IPI, repassado automaticamente às prefeituras segundo faixas populacionais apuradas pelo IBGE.",
    exemploPratico: "Mais de 70% dos municípios brasileiros dependem de repasses como o FPM para pagar despesas básicas locais.",
    fonte: FONTES.senadoOrcamento,
  },
  {
    slug: "quociente-eleitoral",
    termo: "Quociente Eleitoral e Quociente Partidário",
    categoria: "eleicoes",
    categoriaLabel: "Eleições e Partidos",
    emUmaFrase: "A fórmula matemática que divide as vagas de deputados e vereadores entre os partidos.",
    explicacao: "Divide-se o total de votos válidos pelo número de cadeiras em disputa (Quociente Eleitoral). Depois, os votos de cada partido/federação são divididos por esse número (Quociente Partidário) para definir quantas vagas o grupo ganha; as vagas restantes ('sobras') seguem regra proporcional de médias.",
    exemploPratico: "Um candidato com votação gigante puxa colegas do mesmo partido quando o partido atinge múltiplos do Quociente Eleitoral — desde que esses colegas cumpram a cláusula mínima individual.",
    fonte: FONTES.tse,
  },
  {
    slug: "federacao-vs-coligacao",
    termo: "Federação Partidária × Coligação",
    categoria: "eleicoes",
    categoriaLabel: "Eleições e Partidos",
    emUmaFrase: "Coligações valem só para eleição majoritária e duram até a urna; federações atuam juntas por 4 anos inteiros.",
    explicacao: "Desde a reforma eleitoral, partidos não podem mais fazer coligação só para eleger deputados e vereadores. Para somar forças nas eleições proporcionais, precisam formar uma federação nacional e votar juntos no Congresso por toda a legislatura.",
    exemploPratico: "Na hora de calcular o Quociente Eleitoral, todos os partidos dentro de uma mesma federação contam como um bloco único.",
    fonte: FONTES.tse,
  },
  {
    slug: "boletim-de-urna",
    termo: "Boletim de Urna (BU) e QR Code",
    categoria: "eleicoes",
    categoriaLabel: "Eleições e Partidos",
    emUmaFrase: "O extrato impresso em cada seção eleitoral às 17h mostrando todos os votos contados naquela urna.",
    explicacao: "Antes de enviar resultados ao TSE, a urna imprime 5 vias em papel na porta da seção eleitoral e inclui um QR Code assinado digitalmente. Qualquer pessoa pode fotografar e conferir depois se os números no site do TSE batem voto a voto com o papel afixado na escola.",
    exemploPratico: "É o instrumento público mais simples de auditoria cidadã disponível no próprio local de votação.",
    fonte: FONTES.tse,
  },
  {
    slug: "inquerito-arquivado",
    termo: "Inquérito Policial e Inquérito Arquivado",
    categoria: "justica",
    categoriaLabel: "Justiça e Status Processual",
    emUmaFrase: "Fase inicial de investigação — não significa que a pessoa é ré ou culpada; 'arquivado' encerra a apuração sem denúncia.",
    explicacao: "No inquérito, polícia e Ministério Público apuram indícios de um crime. Se não houver base mínima de autoria ou crime após a apuração, o Ministério Público pede o arquivamento e não há ação penal.",
    exemploPratico: "Notícias frequentemente citam 'investigado em inquérito'; é essencial distinguir investigação em curso ou arquivada de processo judicial aberto.",
    fonte: FONTES.stf,
  },
  {
    slug: "reu",
    termo: "Denunciado e Réu",
    categoria: "justica",
    categoriaLabel: "Justiça e Status Processual",
    emUmaFrase: "A pessoa responde a um processo judicial formal em andamento, mas ainda NÃO foi condenada.",
    explicacao: "O Ministério Público apresenta uma denúncia (ou queixa-crime). Só quando um juiz ou tribunal aceita a denúncia por enxergar indícios mínimos é que o investigado se torna 'réu'. Pela Constituição, vale a presunção de inocência durante o processo.",
    exemploPratico: "'Virou réu' indica abertura formal de ação penal ou de improbidade, sem sentença ainda.",
    fonte: FONTES.stf,
  },
  {
    slug: "liminar",
    termo: "Decisão Liminar / Cautelar",
    categoria: "justica",
    categoriaLabel: "Justiça e Status Processual",
    emUmaFrase: "Decisão judicial provisória e urgente tomada antes do julgamento definitivo do processo.",
    explicacao: "Usada quando esperar o julgamento completo poderia causar dano irreversível. Por ser provisória, pode ser confirmada ou derrubada pelos ministros/desembargadores no julgamento do mérito.",
    exemploPratico: "Liminar suspendendo temporariamente uma lei ou ato administrativo até o plenário do tribunal julgar o caso.",
    fonte: FONTES.stf,
  },
  {
    slug: "condenacao-1a-e-2a-instancia",
    termo: "Condenação em 1ª Instância × Órgão Colegiado (2ª Instância)",
    categoria: "justica",
    categoriaLabel: "Justiça e Status Processual",
    emUmaFrase: "Sentença dada por um único juiz (1ª instância) difere de confirmação por um grupo de juízes/desembargadores (colegiado).",
    explicacao: "Na 1ª instância cabe recurso amplo. Quando a condenação criminal ou por improbidade com dolo e lesão ao erário é proferida ou confirmada por órgão colegiado (2ª instância/tribunal), gera inelegibilidade pela Lei da Ficha Limpa — mesmo ainda cabendo recursos excepcionais a tribunais superiores.",
    exemploPratico: "Ao ler qualquer perfil político, verifique sempre em qual instância está eventual condenação e se há recurso suspensivo.",
    fonte: FONTES.tse,
  },
  {
    slug: "transito-em-julgado",
    termo: "Absolvido × Condenação com Trânsito em Julgado",
    categoria: "justica",
    categoriaLabel: "Justiça e Status Processual",
    emUmaFrase: "Decisão definitiva da qual não cabe mais nenhum recurso judicial.",
    explicacao: "Se absolvido, o réu foi considerado inocente (ou não houve prova suficiente de crime). 'Trânsito em julgado' marca o fim definitivo do processo nos tribunais, tornando a decisão imutável salvo ações revisionais excepcionalíssimas.",
    exemploPratico: "Só após condenação definitiva (trânsito em julgado) ou cumprimento de prazos legais ocorre a execução definitiva penal.",
    fonte: FONTES.cf88,
  },
  {
    slug: "prescricao",
    termo: "Processo Prescrito",
    categoria: "justica",
    categoriaLabel: "Justiça e Status Processual",
    emUmaFrase: "Quando o prazo máximo previsto em lei expira antes do fim definitivo do julgamento.",
    explicacao: "Na prescrição, o Estado perde o direito de punir porque o processo ultrapassou o limite legal de tempo. Isso extingue a punibilidade sem equivaler necessariamente a uma declaração de inocência ou culpa no mérito.",
    exemploPratico: "Diferenciar 'absolvido no mérito' de 'prescrito' evita leituras distorcidas em debates eleitorais.",
    fonte: FONTES.stf,
  },
  {
    slug: "lai",
    termo: "Lei de Acesso à Informação (LAI · Lei 12.527/2011)",
    categoria: "cidadania",
    categoriaLabel: "Cidadania e Controle",
    emUmaFrase: "A lei que garante a qualquer cidadão pedir dados e documentos públicos gratuitos sem precisar explicar o motivo.",
    explicacao: "Regra no Estado brasileiro é a transparência; o sigilo é exceção justificada. Órgãos dos três Poderes (União, estados e municípios) têm até 20 dias corridos (prorrogáveis por 10) para entregar a informação ou justificar legalmente o eventual sigilo.",
    exemploPratico: "Pelo sistema Fala.BR você pode solicitar contratos, auditorias, pareceres e planilhas oficiais.",
    fonte: FONTES.falaBr,
  },
  {
    slug: "acao-popular",
    termo: "Ação Popular (Art. 5º, LXXIII da Constituição)",
    categoria: "cidadania",
    categoriaLabel: "Cidadania e Controle",
    emUmaFrase: "Ação judicial ao alcance de qualquer eleitor para anular ato ilegal que prejudique o dinheiro público, o patrimônio ou o meio ambiente.",
    explicacao: "Garantia constitucional de controle cidadão direto: diferente de ações comuns, o autor que age de boa-fé é isento de custas judiciais e honorários de sucumbência.",
    exemploPratico: "Usada por cidadãos para contestar contratos administrativos irregulares ou vendas ilegais de patrimônio público.",
    fonte: FONTES.cf88,
  },
];

export const guiaPorPoder: Record<Poder, GuiaPoder> = {
  legislativo: {
    id: "legislativo",
    nome: "Legislativo",
    corNome: "Verdigris",
    quemIntegra: "União: Câmara dos Deputados (513) e Senado Federal (81) · Estados: Assembleias Legislativas · Municípios: Câmaras Municipais.",
    missaoConstitucional: "Elaborar leis, votar o orçamento público (PPA, LDO e LOA) e fiscalizar as contas e atos do Poder Executivo.",
    oQueFaz: [
      "Discute e aprova leis ordinárias, complementares e emendas à Constituição.",
      "Define em quanto e onde o governo pode gastar no orçamento anual e destina emendas parlamentares.",
      "Fiscaliza ministros e o Executivo por meio de audiências, pedidos de informação, CPIs e auxílio do Tribunal de Contas.",
    ],
    oQueNaoFaz: [
      "Não executa obras nem gerencia hospitais, escolas ou viaturas diretamente (isso cabe ao Executivo).",
      "Não condena nem prende cidadãos em CPI (encaminha indícios ao Ministério Público e Judiciário).",
    ],
    comoFiscalizar: "Acompanhe votações nominais, atuação em comissões, gastos da cota parlamentar (CEAP/CEAPS) e participe das enquetes e do portal e-Cidadania.",
    fonte: FONTES.cf88,
  },
  executivo: {
    id: "executivo",
    nome: "Executivo",
    corNome: "Âmbar",
    quemIntegra: "União: Presidente, Vice e Ministérios · Estados: Governadores e Secretarias · Municípios: Prefeitos e Secretarias.",
    missaoConstitucional: "Administrar a máquina pública no dia a dia, executar o orçamento aprovado pelo Legislativo e chefiar a administração e os serviços públicos.",
    oQueFaz: [
      "Propõe o orçamento anual, envia Projetos de Lei e pode editar Medidas Provisórias em caso de urgência.",
      "Executa políticas de saúde, educação, segurança (nos estados), infraestrutura, transporte e assistência social.",
      "Sanciona ou veta projetos aprovados pelo Legislativo e nomeia ministros/secretários.",
    ],
    oQueNaoFaz: [
      "Não pode criar tributos nem gastar dinheiro público sem lei orçamentária aprovada pelo Legislativo.",
      "Não derruba decisões definitivas do Judiciário nem julga crimes.",
    ],
    comoFiscalizar: "Cobre pelas ouvidorias (Fala.BR, 1746/156/162), consulte contratos nos Portais da Transparência e compare promessas de governo com a execução orçamentária.",
    fonte: FONTES.cf88,
  },
  judiciario: {
    id: "judiciario",
    nome: "Judiciário",
    corNome: "Índigo",
    quemIntegra: "STF (corte constitucional), STJ, Justiça Federal, Trabalhista, Eleitoral, Militar e Tribunais de Justiça dos Estados.",
    missaoConstitucional: "Aplicar as leis em conflitos concretos, julgar ações judiciais com fundamentação e guardar a Constituição (papel central do STF).",
    oQueFaz: [
      "Julga processos individuais e coletivos, garante direitos fundamentais e aplica penalidades quando há previsão legal.",
      "No STF, decide se leis aprovadas pelo Congresso ou atos do Executivo respeitam a Constituição de 1988.",
      "Na Justiça Eleitoral (TSE e TREs), organiza eleições, registra candidaturas e audita urnas e contas de campanha.",
    ],
    oQueNaoFaz: [
      "Não age por iniciativa própria sem provocação externa (princípio da inércia: alguém precisa entrar com ação ou recurso).",
      "Não substitui o Congresso criando impostos ou políticas orçamentárias completas.",
    ],
    comoFiscalizar: "Leia acórdãos e votos inteiros em vez de frases soltas, acompanhe sessões ao vivo na TV Justiça e observe se uma decisão é liminar (provisória) ou definitiva (trânsito em julgado).",
    fonte: FONTES.stf,
  },
};
