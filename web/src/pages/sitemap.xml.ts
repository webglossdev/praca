import type { APIRoute } from "astro";
import { pessoas } from "../data/pessoas";
import { noticias, votacoes } from "../data/portal";

const staticPaths = [
  "/",
  "/pessoas",
  "/comparar",
  "/noticias",
  "/ao-vivo",
  "/partidos",
  "/estados",
  "/busca",
  "/corrigir",
  "/status",
  "/aprender",
  "/guia-do-cidadao",
  "/glossario",
  "/metodologia",
  "/fontes",
  "/dados",
  "/sobre",
  "/privacidade",
  "/termos",
  "/poderes/legislativo",
  "/poderes/executivo",
  "/poderes/judiciario",
  "/institucional/fontes",
  "/institucional/dados",
  "/institucional/sobre",
  "/institucional/privacidade",
  "/institucional/termos",
];

const dynamicPaths = [
  ...pessoas.map((p) => `/pessoas/${p.slug}`),
  ...pessoas.map((p) => `/pessoas/${p.slug}/votos`),
  ...noticias.map((n) => `/noticias/${n.id}`),
  ...votacoes.map((v) => `/votacoes/${v.id}`),
  ...[...new Set(pessoas.map((p) => p.mandatos[0]?.uf).filter((uf): uf is string => Boolean(uf)))].map(
    (uf) => `/estados/${uf.toLowerCase()}`,
  ),
  ...[...new Set(pessoas.map((p) => p.partido?.sigla).filter((sigla): sigla is string => Boolean(sigla)))].map(
    (sigla) => `/partidos/${sigla}`,
  ),
];

const paths = [...new Set([...staticPaths, ...dynamicPaths])];

export const GET: APIRoute = ({ site }) => {
  const base = (site ?? "https://praca.example").toString().replace(/\/$/, "");
  const urls = paths.map((path) => `<url><loc>${base}${path}</loc></url>`).join("");
  return new Response(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urls}</urlset>`, {
    headers: { "Content-Type": "application/xml; charset=utf-8" },
  });
};
