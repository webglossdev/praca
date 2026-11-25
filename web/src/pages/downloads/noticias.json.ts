import type { APIRoute } from "astro";
import { noticias } from "../../data/portal";

export const GET: APIRoute = () =>
  new Response(JSON.stringify(noticias, null, 2) + "\n", {
    headers: { "Content-Type": "application/json; charset=utf-8" },
  });
