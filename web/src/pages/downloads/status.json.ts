import type { APIRoute } from "astro";
import { statusColetores } from "../../data/portal";

export const GET: APIRoute = () =>
  new Response(JSON.stringify(statusColetores, null, 2) + "\n", {
    headers: { "Content-Type": "application/json; charset=utf-8" },
  });
