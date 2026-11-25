import type { APIRoute } from "astro";
import { votacoes } from "../../data/portal";

export const GET: APIRoute = () =>
  new Response(JSON.stringify(votacoes, null, 2) + "\n", {
    headers: { "Content-Type": "application/json; charset=utf-8" },
  });
