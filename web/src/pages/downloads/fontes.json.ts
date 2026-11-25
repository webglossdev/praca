import type { APIRoute } from "astro";
import fontesJson from "../../../../data/publico/fontes.json";

export const GET: APIRoute = () =>
  new Response(JSON.stringify(fontesJson, null, 2) + "\n", {
    headers: { "Content-Type": "application/json; charset=utf-8" },
  });
