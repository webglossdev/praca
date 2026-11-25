import aoVivoJson from "../../../data/publico/fixtures/ao-vivo.json";
import correcoesJson from "../../../data/publico/fixtures/correcoes.json";
import noticiasJson from "../../../data/publico/fixtures/noticias.json";
import statusJson from "../../../data/publico/fixtures/status.json";
import votacoesJson from "../../../data/publico/fixtures/votacoes.json";
import fontesJson from "../../../data/publico/fontes.json";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import type { Poder, Proveniencia } from "./pessoas";

export const SECOES_SENSIVEIS_ATIVAS = false;

export interface Noticia {
  id: string;
  titulo: string;
  veiculo: string;
  publicado_em: string;
  url: string;
  trecho: string;
  pessoa_pids: string[];
  poder: Poder | null;
  tema: string | null;
  tipo_fonte: "oficial" | "imprensa";
  licenca_texto_integral: string | null;
  corpo_integral: string[];
}

export interface Votacao {
  id: string;
  proposicao_id: string;
  data: string;
  resultado: string;
  casa: "camara" | "senado" | string | null;
  proposicao_label: string | null;
  titulo: string | null;
  tema: string | null;
  url: string | null;
  votos: {
    pid: string;
    escolha: "sim" | "nao" | "abstencao" | "ausente" | "obstrucao";
    nome?: string | null;
    partido?: string | null;
    uf?: string | null;
  }[];
}

export interface EventoAoVivo {
  id: string;
  poder: Poder;
  orgao: string;
  titulo: string;
  status: "ao_vivo" | "agendado" | "encerrado" | "indisponivel";
  horario: string;
  pauta: string;
  youtube_id: string | null;
  fonte: Proveniencia<string>;
}

export interface AoVivoEstado {
  emSessao: boolean;
  atualizadoEm: string;
  eventos: EventoAoVivo[];
}

export interface CorrecaoPublica {
  id: string;
  data: string;
  pagina: string;
  campo: string;
  alteracao: string;
  motivo: string;
  fonte_url: string;
}

export interface StatusColetor {
  fonte_id: string;
  nome: string;
  status: "ativa" | "degradada" | "quebrada" | "planejada";
  ultima_coleta: string | null;
  latencia_ms: number | null;
  circuit_breaker: "fechado" | "aberto" | "meio_aberto";
  observacao: string;
}

export interface FonteCatalogo {
  id: string;
  nome: string;
  url: string;
  licenca: string;
  frequencia: string;
}

const dataMode = import.meta.env.PRACA_DATA_MODE ?? "publico";
const publicDir = resolve(process.cwd(), "data/publico");

function carregarPublico<T>(nome: string, fixture: T): T {
  if (dataMode !== "publico") return fixture;
  const caminho = resolve(publicDir, nome);
  if (!existsSync(caminho)) return fixture;
  return JSON.parse(readFileSync(caminho, "utf8")) as T;
}

export const noticias = carregarPublico<Noticia[]>("noticias.json", noticiasJson as Noticia[]);
export const votacoes = carregarPublico<Votacao[]>("votacoes.json", votacoesJson as Votacao[]);
export const aoVivo = carregarPublico<AoVivoEstado>("ao-vivo.json", aoVivoJson as AoVivoEstado);
export const correcoes = carregarPublico<CorrecaoPublica[]>("correcoes.json", correcoesJson as CorrecaoPublica[]);
export const statusColetores = carregarPublico<StatusColetor[]>("status.json", statusJson as StatusColetor[]);
export const fontes = fontesJson.fontes as FonteCatalogo[];
export const DATA_COLETA_REFERENCIA = "2026-10-05";

export const institucionalPaginas: Record<
  string,
  { titulo: string; resumo: string; texto: string }
> = {
  fontes: {
    titulo: "Fontes e licenças",
    resumo: "Todas as fontes públicas integradas no catálogo do Praça, URLs e frequência de atualização.",
    texto: "Cada dado exibido no Praça carrega a identificação da fonte pública original, URL verificável, data/hora de coleta em ISO 8601 e termos de licença.",
  },
  dados: {
    titulo: "Downloads e schema aberto",
    resumo: "Baixe os dados públicos em JSON UTF-8 e valide com o JSON Schema v1.",
    texto: "Os dados públicos são gerados pelo pipeline em Python com validação estrita em Pydantic v2 antes da publicação estática.",
  },
  sobre: {
    titulo: "Sobre o Praça",
    resumo: "Projeto independente e gratuito de transparência cívica e educação política no Brasil.",
    texto: "O Praça reúne dados oficiais dos Três Poderes e explicadores didáticos em uma interface rápida, citável, responsiva e auditável.",
  },
  privacidade: {
    titulo: "Privacidade e zero rastreamento",
    resumo: "Não usamos cookies de terceiros, analytics invasivos nem telemetria.",
    texto: "O Praça usa dados manifestamente públicos de agentes políticos para finalidade cívico-informacional. A preferência local de tema claro/escuro é a única configuração salva no navegador. Incorporações de vídeo em /ao-vivo só são carregadas após clique. Contato, base legal, finalidade, retenção, direitos LGPD e canal de incidentes devem ser publicados pelo responsável antes do lançamento público.",
  },
  termos: {
    titulo: "Termos de uso e direito de resposta",
    resumo: "Código sob AGPL-3.0; dados compilados respeitam a licença de cada fonte oficial.",
    texto: "Não republicamos matérias jornalísticas protegidas sem licença aberta compatível. Notícias de terceiros exibem título, veículo, data, trecho curto e link. Correções e direito de resposta podem ser solicitados em /corrigir com fonte verificável. Processos, suspeitas e ligações ficam desligados até revisão jurídica; consulte JURIDICO.md.",
  },
};
