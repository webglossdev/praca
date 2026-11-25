// SPDX-License-Identifier: AGPL-3.0-or-later

export interface Env {
  ALLOWED_ORIGIN?: string;
  CACHE_TTL_SECONDS?: string;
}

interface EventoLive {
  id: string;
  poder: "legislativo" | "executivo" | "judiciario";
  orgao: string;
  titulo: string;
  status: "ao_vivo" | "agendado" | "encerrado" | "indisponivel";
  horario: string;
  pauta: string;
  youtube_id: string | null;
  fonte: {
    valor: string;
    fonte_id: string;
    url: string;
    coletado_em: string;
    licenca: string;
  };
}

async function fetchJsonSafe(url: string, timeoutMs = 4500): Promise<unknown> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(url, {
      signal: controller.signal,
      headers: { accept: "application/json", "user-agent": "praca-worker/0.1" },
    });
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  } finally {
    clearTimeout(timer);
  }
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    const corsOrigin = env.ALLOWED_ORIGIN || "*";
    const ttl = Math.max(30, Number(env.CACHE_TTL_SECONDS || "60") || 60);

    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: {
          "access-control-allow-origin": corsOrigin,
          "access-control-allow-methods": "GET, OPTIONS",
        },
      });
    }

    if (url.pathname !== "/api/ao-vivo") {
      return new Response(JSON.stringify({ erro: "Rota não encontrada" }), {
        status: 404,
        headers: { "content-type": "application/json; charset=utf-8" },
      });
    }

    const cache = caches.default;
    const cacheKey = new Request(url.toString(), request);
    const cached = await cache.match(cacheKey);
    if (cached) return cached;

    const hoje = new Date().toISOString().slice(0, 10);
    const camaraUrl = `https://dadosabertos.camara.leg.br/api/v2/eventos?dataInicio=${hoje}&dataFim=${hoje}&ordem=ASC&ordenarPor=dataHoraInicio&itens=10`;
    const camaraData = (await fetchJsonSafe(camaraUrl)) as {
      dados?: Array<{ id?: number; descricaoTipo?: string; situacao?: string; dataHoraInicio?: string; orgaos?: Array<{ sigla?: string }> }>;
    } | null;

    const eventos: EventoLive[] = [];
    for (const item of camaraData?.dados ?? []) {
      const situacao = (item.situacao || "").toLowerCase();
      const status = situacao.includes("andamento") ? "ao_vivo" : "agendado";
      eventos.push({
        id: `cam-${item.id ?? eventos.length}`,
        poder: "legislativo",
        orgao: item.orgaos?.[0]?.sigla ? `Câmara (${item.orgaos[0].sigla})` : "Câmara dos Deputados",
        titulo: item.descricaoTipo || "Evento oficial",
        status,
        horario: item.dataHoraInicio || hoje,
        pauta: item.descricaoTipo || "",
        youtube_id: null,
        fonte: {
          valor: "Câmara dos Deputados",
          fonte_id: "camara",
          url: "https://dadosabertos.camara.leg.br/api/v2/eventos",
          coletado_em: new Date().toISOString(),
          licenca: "Dados abertos",
        },
      });
    }

    const body = {
      emSessao: eventos.some((e) => e.status === "ao_vivo"),
      atualizadoEm: new Date().toISOString(),
      degradado: camaraData === null,
      eventos,
    };

    const response = new Response(JSON.stringify(body, null, 2), {
      headers: {
        "content-type": "application/json; charset=utf-8",
        "cache-control": `public, max-age=${ttl}, s-maxage=${ttl}`,
        "access-control-allow-origin": corsOrigin,
      },
    });
    ctx.waitUntil(cache.put(cacheKey, response.clone()));
    return response;
  },
};
