import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import pessoasFixturesJson from "../../../data/publico/fixtures/pessoas.json";

export type Poder = "legislativo" | "executivo" | "judiciario";

export interface Proveniencia<T = string | number> {
  valor: T;
  fonte_id: string;
  url: string;
  coletado_em: string;
  licenca: string;
}

export interface Mandato {
  poder: Poder;
  cargo: string;
  uf: string | null;
  inicio: string;
  fim: string | null;
  status: string;
  titular_pid?: string | null;
}

export interface Filiacao {
  pid: string;
  partido_sigla: string;
  inicio: string;
  fim: string | null;
  fonte: Proveniencia<string>;
}

export interface Proposicao {
  id: string;
  casa: string;
  tipo: string;
  numero: number;
  ano: number;
  ementa: string;
  url: string;
}

export interface VotoNominal {
  votacao_id: string;
  proposicao_label: string;
  tema: string;
  data: string;
  escolha: "sim" | "nao" | "abstencao" | "ausente" | "obstrucao";
  orientacao_partido?: string | null;
  orientacao_governo?: string | null;
  resultado: string;
  url: string;
}

export interface Despesa {
  pid: string;
  categoria: string;
  valor: string | number;
  competencia: string;
  fonte: Proveniencia<string | number>;
}

export interface Emenda {
  parlamentar_pid: string;
  favorecido: string;
  valor_empenhado: string | number;
  ano: number;
  fonte: Proveniencia<string | number>;
}

export interface Doacao {
  candidato_pid: string;
  doador: string;
  valor: string | number;
  ano_eleitoral: number;
  fonte: Proveniencia<string | number>;
}

export interface Bem {
  pid: string;
  descricao: string;
  valor: string | number;
  ano_eleitoral: number;
  fonte: Proveniencia<string | number>;
}

export interface SancaoEmpresa {
  cnpj: string;
  razao_social: string;
  cadastro: string;
  motivo: string;
  data_inicio: string;
  data_fim?: string | null;
  fonte: Proveniencia<string>;
}

export interface Posicionamento {
  autodeclaracao?: Proveniencia<string> | null;
  alinhamento_partido_pct?: number | null;
  alinhamento_governo_pct?: number | null;
  classificacao_partido?: Proveniencia<string> | null;
  metodologia_url: string;
}

export interface PesquisaEleitoral {
  registro_tse: string;
  instituto: string;
  cargo: string;
  data_divulgacao: string;
  margem_erro_pp: number;
  confianca_pct: number;
  percentual_candidato: number;
  fonte: Proveniencia<string>;
}

export interface Atribuicao {
  noticia_id: string;
  rotulo: string;
  desfecho?: string | null;
  atualizado_em?: string | null;
  status?: string | null;
  titulo_noticia?: string | null;
  veiculo?: string | null;
  data?: string | null;
  url?: string | null;
}

export interface Pessoa {
  pid: string;
  nome: string;
  nome_publico: string;
  slug: string;
  mandatos: Mandato[];
  partido: {
    sigla: string;
    nome: string;
    numero: number | null;
    federacao: string | null;
    historico_nomes: string[];
  } | null;
  apelidos: string[];
  fontes: Proveniencia<string>[];
  biografia?: Proveniencia<string> | null;
  resumo_numeros?: Record<string, Proveniencia<string>>;
  filiacoes?: Filiacao[];
  proposicoes?: Proposicao[];
  votos_recentes?: VotoNominal[];
  despesas?: Despesa[];
  emendas?: Emenda[];
  doacoes?: Doacao[];
  bens?: Bem[];
  sancoes_empresas?: SancaoEmpresa[];
  posicionamento?: Posicionamento | null;
  plano_governo?: Proveniencia<string> | null;
  pesquisas?: PesquisaEleitoral[];
  noticias_ids?: string[];
  atribuicoes?: Atribuicao[];
}

const dataMode = import.meta.env.PRACA_DATA_MODE ?? "publico";
const publicPeoplePath = resolve(process.cwd(), "data/publico/pessoas.json");
const publicPeople = dataMode === "publico" && existsSync(publicPeoplePath)
  ? JSON.parse(readFileSync(publicPeoplePath, "utf8"))
  : pessoasFixturesJson;

export const pessoas = publicPeople as unknown as Pessoa[];

export function initials(name: string): string {
  const parts = name
    .split(/\s+/)
    .filter(Boolean)
  if (parts.length === 0) return "";
  if (parts.length === 1) return parts[0].slice(0, 1).toUpperCase();
  return `${parts[0][0]}${parts.at(-1)?.[0] ?? ""}`.toUpperCase();
}

export function formatBrl(value: string | number): string {
  const num = typeof value === "number" ? value : Number(value);
  if (Number.isNaN(num)) return String(value);
  return num.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}
